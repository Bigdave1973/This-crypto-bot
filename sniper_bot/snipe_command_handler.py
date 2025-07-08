# sniper_command_handler.py

import time
import requests
from sniper_command_router import handle_sniper_command  # contains your logic

TELEGRAM_TOKEN = "6361313977:AAE_A8rsFCQn8VY4dXs4VFu1I7cd8RAI96Q"
TELEGRAM_CHAT_ID = "5530664702"
API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def start_command_listener():
    print("🛰️ Telegram command listener started...")
    last_update_id = None

    while True:
        try:
            response = requests.get(f"{API_URL}/getUpdates", timeout=10)
            updates = response.json().get("result", [])

            for update in updates:
                if "message" not in update:
                    continue

                message = update["message"]
                if "text" not in message:
                    continue  # skip non-text messages

                text = message["text"]
                chat_id = message["chat"]["id"]

                print("🔔 Message received:", text)
                print("📩 Chat ID:", chat_id)

                if str(chat_id) != str(TELEGRAM_CHAT_ID):
                    print("❌ Ignored message from unknown chat:", chat_id)
                    continue

                def send_response(reply_text):
                    requests.post(f"{API_URL}/sendMessage", data={
                        "chat_id": chat_id,
                        "text": reply_text
                    })

                handle_sniper_command(text, send_response)
                last_update_id = update["update_id"]

        except Exception as e:
            print("❗ Command listener error:", e)
            time.sleep(3)
