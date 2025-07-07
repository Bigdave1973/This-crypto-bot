import time

def simulate_trade_execution(signal, confidence):
    trade = {
        "pair": signal["pair"],
        "direction": signal["direction"],
        "entry_price": signal["entry"],
        "confidence": confidence,
        "risk_level": signal.get("risk", "unknown"),
        "strategy": signal.get("strategy", "unknown"),
        "status": "OPEN",
        "timestamp": time.time()
    }
    return trade
