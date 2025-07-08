# utils.py

import random

def calculate_rr(entry, sl, tp, direction):
    risk = abs(entry - sl)
    reward = abs(tp - entry)
    if risk == 0:
        return 0
    return round(reward / risk, 2)

def get_trend_alignment(symbol, direction):
    # In real version, pull multi-timeframe trend from real data
    # For now, simulate with randomness
    if direction.lower() == "long":
        return {
            "1W": random.choice([True, False]),
            "1D": random.choice([True, False]),
            "4H": random.choice([True, False])
        }
    else:
        return {
            "1W": random.choice([True, False]),
            "1D": random.choice([True, False]),
            "4H": random.choice([True, False])
        }

def check_rejection(symbol, direction):
    # Mock wick detection — real version uses candle data
    return random.random() > 0.3  # 70% chance there's some wick rejection

def score_confidence(rr, trend, wick):
    score = 50
    if rr >= 2.0:
        score += 15
    elif rr >= 1.5:
        score += 5

    if trend["1W"]:
        score += 10
    if trend["1D"]:
        score += 10
    if trend["4H"]:
        score += 10

    if wick:
        score += 15

    return min(score, 100)
