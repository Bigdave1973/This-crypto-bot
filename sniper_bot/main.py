# main.py

from config import CONFIG
from market_reader import fetch_market_data
from meme_filter import is_meme_coin, strict_meme_filter
from trade_engine import analyze_trade, simulate_trade
from notifier import send_trade_alert
from trade_memory import update_trade_memory, summarize_trades
from webhook_handler import process_webhook_signal
import time
import traceback

print("🔫 Sniper Bot Activated")

def run_bot():
    while True:
        try:
            market_data = fetch_market_data(CONFIG["pairs"])

            for pair, data in market_data.items():
                is_meme = is_meme_coin(pair)

                trade_decision = analyze_trade(data, is_meme)
                if trade_decision["valid"]:
                    if is_meme and not strict_meme_filter(data, trade_decision):
                        continue  # Block weak meme trades
                    
                    trade = simulate_trade(pair, trade_decision)
                    update_trade_memory(trade)
                    send_trade_alert(trade)
        
            time.sleep(CONFIG["scan_interval"])

        except Exception as e:
            with open("logs/errors.log", "a") as f:
                f.write(traceback.format_exc() + "\n")
            time.sleep(5)

if __name__ == "__main__":
    run_bot()
