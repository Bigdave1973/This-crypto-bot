import time
from utils import calculate_rr, get_trend_alignment, check_rejection, score_confidence
from meme_filter import is_meme_coin

CONFIDENCE_THRESHOLD = 80
CONSIDERING_THRESHOLD = 60

def analyze_trade(data, is_meme=False, is_manual=False):
    """
    Analyzes a trade and returns whether it should be taken,
    along with the confidence score and reason.
    Handles both manual and live trades.
    """
    direction = data["direction"]
    symbol = data.get("symbol") or data.get("pair") or "UNKNOWN"

    # 🧠 Set entry, SL, TP
    if is_manual:
        entry = data["entry"]
        sl = data["sl"]
        tp = data["tp"]
    else:
        entry = data.get("entry") or data.get("price") or data.get("close")
        sl = entry * 0.98 if direction == "LONG" else entry * 1.02
        tp = entry * 1.04 if direction == "LONG" else entry * 0.96

    rr = calculate_rr(entry, sl, tp, direction)
    trend_match = get_trend_alignment(symbol, direction)
    wick_reject = check_rejection(symbol, direction)
    confidence = score_confidence(rr, trend_match, wick_reject)

    # Reason generator
    reason_parts = []
    if wick_reject:
        reason_parts.append("Wick rejection")
    if trend_match.get("1W"):
        reason_parts.append("1W trend match")
    if trend_match.get("1D"):
        reason_parts.append("1D trend match")
    if trend_match.get("4H"):
        reason_parts.append("4H trend match")
    if rr >= 2.0:
        reason_parts.append("Good R:R")

    reason = ", ".join(reason_parts) if reason_parts else "Weak setup"

    # 🚫 MEME Coin strict filter
    if is_meme:
        if confidence < CONFIDENCE_THRESHOLD or rr < 1.8 or not wick_reject:
            return {
                "valid": False,
                "confidence": confidence,
                "rr": rr,
                "reason": "Meme coin rejected: confidence, R:R, or wick issue",
                "considering": False,
                "is_meme": True,
                "direction": direction
            }

    # ✅ Valid trade
    if confidence >= CONFIDENCE_THRESHOLD:
        return {
            "valid": True,
            "confidence": confidence,
            "rr": rr,
            "reason": reason,
            "is_meme": is_meme,
            "considering": False,
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "direction": direction
        }

    # ⚠️ Considering stage
    if confidence >= CONSIDERING_THRESHOLD and rr >= 1.5:
        return {
            "valid": False,
            "confidence": confidence,
            "rr": rr,
            "reason": reason,
            "considering": True,
            "is_meme": is_meme,
            "entry": entry,
            "direction": direction
        }

    # ❌ Full rejection
    return {
        "valid": False,
        "confidence": confidence,
        "rr": rr,
        "reason": "Low confidence or bad R:R",
        "considering": False,
        "is_meme": is_meme,
        "direction": direction
    }

def simulate_trade(pair, trade_data):
    """
    Simulates a trade and returns the trade structure used for tracking.
    """
    return {
        "pair": pair,
        "direction": trade_data.get("direction"),
        "entry": trade_data.get("entry"),
        "sl": trade_data.get("sl"),
        "tp": trade_data.get("tp"),
        "confidence": trade_data.get("confidence", 0),
        "rr": trade_data.get("rr", 0),
        "status": "open",
        "timestamp": time.time(),
        "is_meme": trade_data.get("is_meme", False)
    }
