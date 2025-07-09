# trade_engine.py

import random
from config import DEFAULT_CAPITAL
from memory import add_open_trade

def analyze_manual_trade(pair):
    """
    Simulate analyzing a manual trade request.
    Returns whether bot would take it or not.
    """

    # ⚠️ TEMP MOCK — later replace with real market logic
    confidence = random.randint(60, 95)
    rr = round(random.uniform(1.5, 3.5), 2)
    direction = random.choice(["LONG", "SHORT"])
    reason = "Strong setup detected on multiple timeframes"

    if confidence < 70 or rr < 1.8:
        return {
            "valid": False,
            "reason": "Low confidence or R:R"
        }

    # Simulate trade tracking
    trade = {
        "pair": pair,
        "type": direction,
        "entry_price": 0,  # to be updated by live price later
        "rr": rr,
        "confidence": confidence,
        "reason": reason,
        "capital": DEFAULT_CAPITAL,
        "friend_trade": True,
    }

    add_open_trade(trade)

    return {
        "valid": True,
        "confidence": confidence,
        "rr": rr,
        "direction": direction,
        "reason": reason
    }

def analyze_live_market(bot):
    """
    Placeholder: scans all active pairs and simulates market reading
    """
    # You’ll replace this with the real logic later
    print("📡 Scanning market... (live logic not yet added)")
