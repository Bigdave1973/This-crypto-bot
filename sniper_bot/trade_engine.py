# trade_engine.py

from utils import calculate_rr, get_trend_alignment, check_rejection, score_confidence
from meme_filter import is_meme_coin

CONFIDENCE_THRESHOLD = 80
CONSIDERING_THRESHOLD = 60

def analyze_trade(data, is_meme=False, is_manual=False):
    """
    Analyzes a trade and returns whether it should be taken,
    along with the confidence score and reason.
    """
    entry = data["entry"]
    sl = data["sl"]
    tp = data["tp"]
    direction = data["direction"]
    symbol = data["symbol"] if "symbol" in data else data.get("pair")

    rr = calculate_rr(entry, sl, tp, direction)
    trend_match = get_trend_alignment(symbol, direction)
    wick_reject = check_rejection(symbol, direction)

    confidence = score_confidence(rr, trend_match, wick_reject)

    # Reason
    reason_parts = []
    if wick_reject:
        reason_parts.append("Wick rejection")
    if trend_match["1W"]:
        reason_parts.append("1W trend match")
    if trend_match["1D"]:
        reason_parts.append("1D trend match")
    if trend_match["4H"]:
        reason_parts.append("4H trend match")
    if rr >= 2.0:
        reason_parts.append("Good R:R")

    reason = ", ".join(reason_parts) if reason_parts else "Weak setup"

    # MEME filter stricter logic
    if is_meme:
        if confidence < CONFIDENCE_THRESHOLD or rr < 1.8 or not wick_reject:
            return {
                "valid": False,
                "confidence": confidence,
                "rr": rr,
                "reason": "Meme coin rejected: confidence, R:R, or wick issue",
                "considering": False,
                "is_meme": True
            }

    # VALID TRADE
    if confidence >= CONFIDENCE_THRESHOLD:
        return {
            "valid": True,
            "confidence": confidence,
            "rr": rr,
            "reason": reason,
            "is_meme": is_meme,
            "considering": False
        }

    # CONSIDERING STAGE
    if confidence >= CONSIDERING_THRESHOLD and rr >= 1.5:
        return {
            "valid": False,
            "confidence": confidence,
            "rr": rr,
            "reason": reason,
            "considering": True,
            "is_meme": is_meme
        }

    # FULL REJECTION
    return {
        "valid": False,
        "confidence": confidence,
        "rr": rr,
        "reason": "Low confidence or bad R:R",
        "considering": False,
        "is_meme": is_meme
    }
