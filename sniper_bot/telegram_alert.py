# telegram_alert.py

import requests
from config import CONFIG

def send_telegram_alert(trade, stage="confirmed"):
    token = CONFIG["telegram"]["bot_token"]
    chat_id = CONFIG["telegram"]["chat_id"]

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
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram alert failed:", e)
