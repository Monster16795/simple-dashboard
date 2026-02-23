from flask import Flask, render_template_string, request, redirect, url_for
from strategy import generate_signals
import os
# -----------------------------
# GLOBAL VARIABLES
# -----------------------------
signals = []            # your stock signals list (can start empty or with dummy data)
auto_trading = True     # Auto Trading state (True = ON, False = OFF)
overrides = {}          # manual overrides dictionary (LONG / SHORT / IGNORE)
app = Flask(__name__)

# In-memory overrides and auto-trading flag
overrides = {}  # symbol -> "LONG"/"SHORT"/"IGNORE"
auto_trading = True

HTML = """
<meta http-equiv="refresh" content="60">
<h1>Automated Trading Dashboard (Real Signals)</h1>

<form method="post" action="/toggle_auto">
    <button type="submit">{{ 'Auto Trading ON' if auto_trading else 'Auto Trading OFF' }}</button>
</form>

<table border="1" cellpadding="5">
<tr>
<th>Symbol</th><th>Signal</th><th>Direction</th><th>Trend</th>
<th>Entry</th><th>Stop</th><th>Session</th><th>Override</th>
<tr style="
{% if s.symbol in overrides %}
    {% if overrides[s.symbol] == 'LONG' %}background-color:#b6fcb6;
    {% elif overrides[s.symbol] == 'SHORT' %}background-color:#fcb6b6;
    {% elif overrides[s.symbol] == 'IGNORE' %}background-color:#f0f0f0;
    {% endif %}
{% endif %}
">
{% for s in signals %}
<tr>
<td>{{ s.symbol }}</td>
<td>{{ s.signal }}</td>
<td>{{ s.direction }}</td>
<td>{{ s.trend }}</td>
<td>{{ s.entry }}</td>
<td>{{ s.stop }}</td>
<td>{{ s.session }}</td>
<td>
    <form method="post" action="/override">
        <input type="hidden" name="symbol" value="{{ s.symbol }}">
        <button name="action" value="LONG">LONG</button>
        <button name="action" value="SHORT">SHORT</button>
        <button name="action" value="IGNORE">IGNORE</button>
    </form>
</td>
</tr>
{% endfor %}
</table>
"""

@app.route("/")
def dashboard():
    return render_template_string(
        HTML,
        signals=signals,
        auto_trading=auto_trading,
        overrides=overrides   # <--- pass the overrides dictionary to template
    )
    try:
        signals = generate_signals()
    except Exception as e:
        print(f"Error generating signals: {e}")
        signals = [{"symbol":"ERROR","signal":"-","direction":"-","trend":"-",
                    "entry":"-","stop":"-","session":"-"}]

    # Apply overrides
    for s in signals:
        if s["symbol"] in overrides:
            override = overrides[s["symbol"]]
            if override == "IGNORE":
                s["signal"] = "IGNORED"
                s["direction"] = "-"
                s["trend"] = "-"
            else:
                s["direction"] = override
                s["trend"] = "Bull" if override=="LONG" else "Bear"
                s["signal"] = "OVERRIDE"
    return render_template_string(HTML, signals=signals, auto_trading=auto_trading)

@app.route("/override", methods=["POST"])
def override():
    symbol = request.form.get("symbol")
    action = request.form.get("action")
    overrides[symbol] = action
    return redirect(url_for("dashboard"))

@app.route("/toggle_auto", methods=["POST"])
def toggle_auto():
    global auto_trading
    auto_trading = not auto_trading
    return redirect(url_for("dashboard"))

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
