from flask import Flask, render_template_string
import os

app = Flask(__name__)

# --- Fake signals for testing ---
FAKE_SIGNALS = [
    {"symbol": "AAPL", "signal": "SETUP", "direction": "LONG", "trend": "Bull", "entry": "-", "stop": "-", "session": "RTH"},
    {"symbol": "MSFT", "signal": "TRIGGER", "direction": "SHORT", "trend": "Bear", "entry": "300.50", "stop": "305.00", "session": "RTH"},
    {"symbol": "NVDA", "signal": "SETUP", "direction": "LONG", "trend": "Bull", "entry": "-", "stop": "-", "session": "Extended"},
]

HTML = """
<meta http-equiv="refresh" content="60">
<h1>Automated Trading Dashboard (Fake Signals)</h1>

<table border="1" cellpadding="5">
<tr><th>Symbol</th><th>Signal</th><th>Direction</th><th>Trend</th><th>Entry</th><th>Stop</th><th>Session</th></tr>
{% for s in signals %}
<tr>
<td>{{ s.symbol }}</td>
<td>{{ s.signal }}</td>
<td>{{ s.direction }}</td>
<td>{{ s.trend }}</td>
<td>{{ s.entry }}</td>
<td>{{ s.stop }}</td>
<td>{{ s.session }}</td>
</tr>
{% endfor %}
</table>
"""

@app.route("/")
def dashboard():
    return render_template_string(HTML, signals=FAKE_SIGNALS)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
