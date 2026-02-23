   from flask import Flask, render_template_string
from strategy import generate_signals
import os

app = Flask(__name__)

HTML = """
<meta http-equiv="refresh" content="60">
<h1>Automated Trading Dashboard (Real Signals)</h1>

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
    signals = generate_signals()
    return render_template_string(HTML, signals=signals)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
