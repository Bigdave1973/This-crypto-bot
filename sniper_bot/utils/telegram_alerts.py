import requests
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Telegram error: {response.text}")
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")
