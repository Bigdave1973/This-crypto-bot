# meme_filter.py

import json
from config import CONFIG

MEME_FLAGS_FILE = "pairs/meme_flags.json"

def load_manual_meme_flags():
    try:
        with open(MEME_FLAGS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def is_meme_coin(pair):
    coin = pair.replace("USDT", "")
    manual_flags = load_manual_meme_flags()
    return manual_flags.get(coin, coin in CONFIG["meme_coins"])

def strict_meme_filter(data, decision):
    """
    Enforce stricter rules for meme trades:
    - Confidence ≥ required
    - Wick rejection detected
    - Multi-timeframe trend match
    - R:R ≥ minimum
    """
    confidence = decision.get("confidence", 0)
    rr = decision.get("rr", 0)
    wick = decision.get("wick_rejection", False)
    trend_match = decision.get("trend_match", False)

    if confidence < CONFIG["risk"]["meme_trade_min_confidence"]:
        return False
    if rr < CONFIG["risk"]["meme_rr"]:
        return False
    if not wick:
        return False
    if not trend_match:
        return False

    return True

def mark_meme(coin_name):
    flags = load_manual_meme_flags()
    flags[coin_name] = True
    with open(MEME_FLAGS_FILE, "w") as f:
        json.dump(flags, f, indent=2)

def unmark_meme(coin_name):
    flags = load_manual_meme_flags()
    if coin_name in flags:
        del flags[coin_name]
        with open(MEME_FLAGS_FILE, "w") as f:
            json.dump(flags, f, indent=2)
