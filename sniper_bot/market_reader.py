# market_reader.py

import ccxt
import pandas as pd
import time

exchange = ccxt.binance()

def fetch_market_data(pairs):
    """
    Fetch real-time price, RSI, wick rejection, and trend match for each pair.
    """
    market_data = {}

    for pair in pairs:
        try:
            formatted_pair = format_pair(pair)
            ohlcv = exchange.fetch_ohlcv(formatted_pair, timeframe="5m", limit=20)
            df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])

            df["rsi"] = compute_rsi(df["close"], 14)

            latest = df.iloc[-1]
            prev = df.iloc[-2]

            market_data[pair] = {
                "price": latest["close"],
                "rsi": round(latest["rsi"], 2),
                "wick_rejection": detect_wick_rejection(latest, prev),
                "trend_match": detect_trend(df)
            }

        except Exception as e:
            print(f"❌ Error fetching {pair}: {e}")
            time.sleep(1)

    return market_data

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def detect_wick_rejection(latest, prev):
    body = abs(latest["close"] - latest["open"])
    upper_wick = latest["high"] - max(latest["close"], latest["open"])
    lower_wick = min(latest["close"], latest["open"]) - latest["low"]
    wick = max(upper_wick, lower_wick)
    return wick > (1.5 * body)

def detect_trend(df):
    df["ema_5"] = df["close"].ewm(span=5).mean()
    df["ema_20"] = df["close"].ewm(span=20).mean()
    return df["ema_5"].iloc[-1] > df["ema_20"].iloc[-1]

def format_pair(pair):
    if "/" in pair:
        return pair
    if pair.endswith("USDT"):
        return pair.replace("USDT", "/USDT")
    return pair
