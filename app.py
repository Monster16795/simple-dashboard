from flask import Flask, render_template_string, request
import os

# -----------------------------
# GLOBAL VARIABLES
# -----------------------------
signals = [
    {"symbol": "AAPL", "signal": "BUY", "direction": "LONG", "trend": "UP", "entry": 150, "stop": 145, "session": "INTRADAY"},
    {"symbol": "TSLA", "signal": "SELL", "direction": "SHORT", "trend": "DOWN", "entry": 800, "stop": 820, "session": "INTRADAY"},
    {"symbol": "AMZN", "signal": "BUY", "direction": "LONG", "trend": "UP", "entry": 3200, "stop": 3150, "session": "INTRADAY"}
]

auto_trading = True     # Auto Trading ON/OFF
overrides = {}          # Manual override dictionary

# -----------------------------
# INITIALIZE FLASK APP
# -----------------------------
app = Flask(__name__)

# -----------------------------
# HTML TEMPLATE
# -----------------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Trading Dashboard</title>
</head>
<body>
    <h1>Automated Trading Dashboard</h1>
    <p>Auto Trading: {{ 'ON' if auto_trading else 'OFF' }}</p>
    <table border="1">
        <tr>
            <th>Symbol</th>
            <th>Signal</th>
            <th>Direction</th>
            <th>Trend</th>
            <th>Entry</th>
            <th>Stop</th>
            <th>Session</th>
            <th>Override</th>
            <th>Current Override</th>
        </tr>
        {% for s in signals %}
        {% set current = overrides.get(s.symbol.strip(), '') %}
        <tr style="
            {% if current == 'LONG' %}background-color:#b6fcb6;
            {% elif current == 'SHORT' %}background-color:#fcb6b6;
            {% elif current == 'IGNORE' %}background-color:#f0f0f0;
            {% endif %}
        ">
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
            <td>{{ current if current else 'None' }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# -----------------------------
# DASHBOARD ROUTE
# -----------------------------
@app.route("/")
def dashboard():
    return render_template_string(
        HTML,
        signals=signals,
        auto_trading=auto_trading,
        overrides=overrides
    )

# -----------------------------
# OVERRIDE ROUTE
# -----------------------------
@app.route("/override", methods=["POST"])
def override():
    symbol = request.form["symbol"].strip()   # Remove extra spaces
    action = request.form["action"].strip()   # LONG / SHORT / IGNORE
    overrides[symbol] = action
    print("Overrides Updated:", overrides)    # Debug log
    return dashboard()

# -----------------------------
# RUN FLASK ON RENDER PORT
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
