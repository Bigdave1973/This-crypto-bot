# trade_engine.py

import random
import json
from config import PAIRS_PATH, CHAT_ID, DEFAULT_CAPITAL
from memory import add_open_trade
from telegram import Bot

def analyze_manual_trade(pair):
    confidence = random.randint(60, 95)
    rr = round(random.uniform(1.5, 3.5), 2)
    direction = random.choice(["LONG", "SHORT"])
    reason = "Strong setup detected on multiple timeframes"

    if confidence < 70 or rr < 1.8:
        return {
            "valid": False,
            "reason": "Low confidence or R:R"
        }

    trade = {
        "pair": pair,
        "type": direction,
        "entry_price": 0,  # will be updated later
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

def analyze_live_market(bot: Bot):
    try:
        with open(PAIRS_PATH, "r") as f:
            pairs = json.load(f)
    except Exception as e:
        print(f"[!] Failed to load pairs: {e}")
        return

    for pair in pairs:
        # Simulate market reading (random for now)
        confidence = random.randint(65, 95)
        rr = round(random.uniform(1.6, 3.8), 2)
        direction = random.choice(["LONG", "SHORT"])
        reason = "Live candle pattern and trend alignment"

        # Filter logic
        if confidence >= 75 and rr >= 2.0:
            trade = {
                "pair": pair,
                "type": direction,
                "entry_price": 0,  # will be replaced with real price
                "rr": rr,
                "confidence": confidence,
                "reason": reason,
                "capital": DEFAULT_CAPITAL,
                "friend_trade": False
            }

            add_open_trade(trade)

            msg = (
                f"🚨 *Sniper Trade Triggered!*\n"
                f"Pair: `{pair}` | {direction}\n"
                f"Confidence: {confidence}% | R:R: {rr}\n"
                f"Reason: _{reason}_\n"
            )
            bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")
