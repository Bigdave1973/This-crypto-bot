# weekly_summary.py

import os
import zipfile
import requests
from datetime import datetime

# Your real Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = "6204073322:AAH_oZY0RzIQFfxfYJAD3rIWsWhi68u2hxI"
TELEGRAM_CHAT_ID = "5942281679"

def zip_trade_log():
    logs_dir = "logs"
    file_name = "trade_log.json"
    zip_name = f"weekly_trade_summary_{datetime.utcnow().strftime('%Y%m%d')}.zip"

    zip_path = os.path.join(logs_dir, zip_name)
    file_path = os.path.join(logs_dir, file_name)

    if not os.path.exists(file_path):
        print("❌ No trade log found.")
        return None

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, arcname=file_name)

    return zip_path

def send_zip_to_telegram(zip_path):
    if not zip_path:
        return

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        with open(zip_path, "rb") as file:
            requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID}, files={"document": file})
        print(f"✅ Sent weekly trade summary: {zip_path}")
    except Exception as e:
        print(f"❌ Telegram zip send error: {e}")
