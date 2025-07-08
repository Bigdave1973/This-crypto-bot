# trade_engine.py

from config import CONFIG
import random

def analyze_trade(data, is_meme=False):
    """
    Analyze and decide if a trade should be considered.
    """
    price = data.get("price")
    rsi = data.get("rsi")
    wick = data.get("wick_rejection", False)
    trend_match = data.get("trend_match", False)

    # Simulated signal logic — replace with real one later
    direction = "SHORT" if rsi > 70 else "LONG" if rsi < 30 else None
    if not direction:
        return {"valid": False}

    stop_loss = price * (1.015 if direction == "SHORT" else 0.985)
    take_profit = price * (0.97 if direction == "SHORT" else 1.03)
    rr = abs((price - take_profit) / (stop_loss - price))
    confidence = random.randint(65, 95)  # Placeholder for real confidence

    min_rr = CONFIG["risk"]["meme_rr"] if is_meme else CONFIG["risk"]["min_rr"]
    if rr < min_rr:
        return {"valid": False}

    return {
        "valid": True,
        "direction": direction,
        "entry": price,
        "sl": stop_loss,
        "tp": take_profit,
        "rr": round(rr, 2),
        "confidence": confidence,
        "wick_rejection": wick,
        "trend_match": trend_match
    }

def simulate_trade(pair, trade_decision):
    """
    Simulate trade with fixed capital.
    """
    capital = CONFIG["exchange"]["simulated_capital"]
    leverage = CONFIG["exchange"]["leverage"]
    size = capital * leverage
    pnl = calculate_pnl(trade_decision, size)

    return {
        "pair": pair,
        "entry": trade_decision["entry"],
        "sl": trade_decision["sl"],
        "tp": trade_decision["tp"],
        "direction": trade_decision["direction"],
        "confidence": trade_decision["confidence"],
        "rr": trade_decision["rr"],
        "wick_rejection": trade_decision["wick_rejection"],
        "trend_match": trade_decision["trend_match"],
        "pnl": pnl
    }

def calculate_pnl(decision, size):
    direction = decision["direction"]
    entry = decision["entry"]
    tp = decision["tp"]
    sl = decision["sl"]

    if direction == "LONG":
        return round(((tp - entry) / entry) * size, 2)
    else:
        return round(((entry - tp) / entry) * size, 2)
