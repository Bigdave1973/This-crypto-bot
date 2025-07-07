def analyze_market(pair):
    return {
        "trend": "bullish",
        "rsi": 67,
        "retracement_zone": True
    }

def score_trade_confidence(signal, market_data):
    score = 0
    if market_data["trend"] == "bullish":
        score += 30
    if market_data["rsi"] < 70:
        score += 20
    if market_data["retracement_zone"]:
        score += 30
    if signal.get("risk") == "low":
        score += 10
    return min(score, 100)

def validate_trade_risk_reward(signal):
    entry = signal.get("entry")
    sl = signal.get("sl")
    tp = signal.get("tp")
    if not all([entry, sl, tp]): return False
    risk = abs(entry - sl)
    reward = abs(tp - entry)
    return reward / risk >= 1.5
