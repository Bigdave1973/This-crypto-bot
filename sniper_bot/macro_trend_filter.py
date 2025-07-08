# macro_trend_filter.py

import ccxt
import pandas as pd

exchange = ccxt.binance()

def fetch_ema(symbol, timeframe="1d", ema_period=50):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=ema_period + 1)
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["ema"] = df["close"].ewm(span=ema_period).mean()
        return df.iloc[-1]["close"], df.iloc[-1]["ema"]
    except:
        return None, None

def macro_trend_all_match(symbol):
    """
    Only returns True if price is above (or below) all 3 EMAs:
    1W, 1D, and 4H.
    """
    tf_list = [("1w", 50), ("1d", 50), ("4h", 50)]
    trend_match = []

    for tf, period in tf_list:
        close, ema = fetch_ema(symbol, tf, period)
        if close is None or ema is None:
            return False

        if close >= ema:
            trend_match.append("UP")
        else:
            trend_match.append("DOWN")

    # Must all agree
    return all(t == trend_match[0] for t in trend_match)
