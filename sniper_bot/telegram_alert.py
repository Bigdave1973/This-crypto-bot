# telegram_alert.py

import requests

# 🔐 Your bot's token and chat ID
TOKEN = "6157583054:AAE7ZzU1vJjRAUrndfe8q2cZlyxtqO1LugI"
CHAT_ID = 5528791457

def send_telegram_alert(trade, stage="confirmed"):
    """
    Sends Telegram alerts to notify trade status.
    Stages:
      - "considering": thinking about entering
      - "confirmed": trade taken
    """
    if stage == "considering":
        message = (
            f"🧠 *SNIPER CONSIDERING TRADE*\n"
            f"Pair: {trade['pair']}\n"
            f"Direction: {trade['direction']}\n"
            f"Confidence: {trade['confidence']}%\n"
            f"R:R: {trade['rr']}\n"
            f"Reason: {trade['reason']}\n"
        )
    elif stage == "confirmed":
        emoji = "⚠️" if trade.get("is_meme") else "✅"
        message = (
            f"🚨 *TRADE INITIATED ({trade['direction'].upper()})*\n"
            f"{emoji} {trade['pair']}\n"
            f"Entry: {trade['entry']}\n"
            f"SL: {trade['sl']} | TP: {trade['tp']}\n"
            f"R:R: {trade['rr']} | Confidence: {trade['confidence']}%\n"
            f"Reason: {trade['reason']}\n"
        )
    else:
        return  # Unknown stage

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram alert failed:", e)
