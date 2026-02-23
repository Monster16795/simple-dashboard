import alpaca_trade_api as tradeapi
import pandas as pd
import os

# Read API keys from environment
ALPACA_KEY = os.environ.get("ALPACA_API_KEY")
ALPACA_SECRET = os.environ.get("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(ALPACA_KEY, ALPACA_SECRET, BASE_URL, api_version='v2')

# 10-stock watchlist
WATCHLIST = ["AAPL","MSFT","NVDA","AMZN","TSLA","META","GOOGL","JPM","DIS","NFLX"]

def get_intraday_data(symbol, timeframe="15Min", limit=50):
    bars = api.get_bars(symbol, timeframe, limit=limit).df
    return bars

def generate_signals():
    signals = []
    for symbol in WATCHLIST:
        df = get_intraday_data(symbol)
        last_row = df.iloc[-1]
        direction = "LONG" if last_row['close'] > last_row['open'] else "SHORT"
        signals.append({
            "symbol": symbol,
            "signal": "TRIGGER",
            "direction": direction,
            "trend": "Bull" if direction=="LONG" else "Bear",
            "entry": round(last_row['close'], 2),
            "stop": round(last_row['close']*0.99,2) if direction=="LONG" else round(last_row['close']*1.01,2),
            "session": "RTH"
        })
    return signals
