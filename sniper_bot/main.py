# main.py

from market_reader import fetch_market_data
from meme_filter import is_meme_coin, strict_meme_filter
from trade_engine import analyze_trade, simulate_trade
from telegram_alert import send_telegram_alert
from trade_memory import update_trade_memory
from open_trade_tracker import load_open_trades, track_open_trades
from sniper_command_handler import handle_sniper_command
import time
import traceback
import requests

# 🔐 Hardcoded Telegram details
BOT_TOKEN = "6157583054:AAE7ZzU1vJjRAUrndfe8q2cZlyxtqO1LugI"
CHAT_ID = 5528791457

# 🛠 Settings
PAIRS = ["BTC/USDT", "ETH/USDT", "PEPE/USDT"]
SCAN_INTERVAL = 10  # seconds

print("🔫 Sniper Bot Activated")

def process_telegram_commands():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

    try:
        response = requests.get(url)
        result = response.json()["result"]

        for update in result:
            if "message" in update and "text" in update["message"]:
                msg = update["message"]
                text = msg["text"]
                sender = msg["chat"]["id"]

                if sender == CHAT_ID and text.startswith("/sniper"):
                    def send_response(reply):
                        reply_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                        payload = {
                            "chat_id": sender,
                            "text": reply
                        }
                        requests.post(reply_url, data=payload)

                    handle_sniper_command(text, send_response)

                # prevent reprocessing by advancing offset
                offset = update["update_id"] + 1
                requests.get(url + f"?offset={offset}")
    except Exception as e:
        print("Command polling error:", e)

def run_bot():
    load_open_trades()

    while True:
        try:
            # 🔄 Update existing open trades
            track_open_trades()

            # 📩 Check Telegram for new commands
            process_telegram_commands()

            # 📊 Fetch latest market data
            market_data = fetch_market_data(PAIRS)

            for pair, data in market_data.items():
                is_meme = is_meme_coin(pair)

                trade_decision = analyze_trade(data, is_meme)

                # 🧠 If it's being considered (not valid yet), notify
                if not trade_decision["valid"]:
                    if trade_decision.get("considering"):
                        send_telegram_alert({
                            "pair": pair,
                            "direction": data["direction"],
                            "confidence": trade_decision["confidence"],
                            "rr": trade_decision["rr"],
                            "reason": trade_decision["reason"]
                        }, stage="considering")
                    continue

                # 🚫 Block meme trades that don't pass strict filters
                if is_meme and not strict_meme_filter(data, trade_decision):
                    continue

                # ✅ Simulate and track valid trade
                trade = simulate_trade(pair, trade_decision)
                update_trade_memory(trade)
                send_telegram_alert(trade, stage="confirmed")

            time.sleep(SCAN_INTERVAL)

        except Exception as e:
            with open("logs/errors.log", "a") as f:
                f.write(traceback.format_exc() + "\n")
            time.sleep(5)

if __name__ == "__main__":
    run_bot()
