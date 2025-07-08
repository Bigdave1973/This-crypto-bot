# telegram_alert.py

import requests

# 👇 Your real bot credentials
TELEGRAM_BOT_TOKEN = "6204073322:AAH_oZY0RzIQFfxfYJAD3rIWsWhi68u2hxI"
TELEGRAM_CHAT_ID = "5942281679"

def send_telegram_alert(trade):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram credentials missing.")
        return

    pair = trade.get("pair", "N/A")
    direction = trade.get("direction", "N/A")
    entry = trade.get("entry", "N/A")
    sl = trade.get("stop_loss", "N/A")
    tp = trade.get("take_profit", "N/A")
    rr = trade.get("rr", 0)
    confidence = trade.get("confidence", 0)
    reason = trade.get("reason", "Unknown")

    is_meme = trade.get("meme", False)
    warning = "⚠️ High-Risk Asset Detected\n" if is_meme else ""

    msg = f"""
🚨 NEW TRADE INITIATED ({direction.upper()})
🪙 Pair: {pair}
📈 Entry: {entry}
🛡️ Stop Loss: {sl}
🎯 Take Profit: {tp}
📊 R:R: {rr} | 🎯 Confidence: {confidence}%
🧠 Reason: {reason}
{warning}
    """

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg.strip(), "parse_mode": "Markdown"}
        requests.post(url, data=payload)
    except Exception as e:
        print(f"❌ Telegram error: {e}")
