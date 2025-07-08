import requests

BOT_TOKEN = "8162837839:AAEP8UP7Q1lFIZOIXrvfBsmSAZ16STOO0Ss"
CHAT_ID = 941162624

def send_telegram_alert(trade, stage="confirmed"):
    if stage == "considering":
        msg = (
            f"🧐 TRADE SETUP BEING CONSIDERED\n"
            f"{trade['pair']} | {trade['direction']}\n"
            f"Confidence: {trade['confidence']}% | R:R: {trade['rr']}\n"
            f"Reason: {trade['reason']}\n"
        )
    elif stage == "confirmed":
        msg = (
            f"🚨 NEW TRADE INITIATED\n"
            f"🪙 Pair: {trade['pair']}\n"
            f"📈 Direction: {trade['direction']}\n"
            f"🎯 Entry: {trade['entry']}\n"
            f"🛡️ Stop Loss: {trade['sl']}\n"
            f"💰 Take Profit: {trade['tp']}\n"
            f"📊 Confidence: {trade['confidence']}% | R:R: {trade['rr']}\n"
        )
    else:
        msg = "⚠️ Unknown alert stage."

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram alert error:", e)
