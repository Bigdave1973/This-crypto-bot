import time
from config.settings import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    TRADE_INTERVAL_SECONDS,
)
from utils.telegram_alerts import send_telegram_message
from utils.trade_logger import log_trade, log_trade_memory
from utils.risk_manager import check_risk_reward, filter_by_confidence
from strategy.entry_logic import evaluate_market_for_entry
from strategy.exit_logic import evaluate_exit_conditions
from strategy.confidence_score import calculate_confidence_score
from handlers.webhook_handler import handle_external_signal
import json
import os


OPEN_TRADES_FILE = "memory/trade_memory.json"


def load_open_trades():
    if os.path.exists(OPEN_TRADES_FILE):
        with open(OPEN_TRADES_FILE, "r") as file:
            return json.load(file)
    return []


def save_open_trades(trades):
    with open(OPEN_TRADES_FILE, "w") as file:
        json.dump(trades, file, indent=4)


def main():
    print("🤖 Sniper Bot started...")
    send_telegram_message("🚀 Sniper Bot is now live!")

    open_trades = load_open_trades()

    while True:
        # 1. Check for new signal
        signal = evaluate_market_for_entry()

        if signal:
            confidence = calculate_confidence_score(signal)

            if check_risk_reward(signal) and filter_by_confidence(confidence):
                signal["confidence"] = confidence
                signal["status"] = "OPEN"
                open_trades.append(signal)

                send_telegram_message(
                    f"🚨 NEW TRADE INITIATED ({signal['direction'].upper()})\n"
                    f"🪙 Pair: {signal['pair']}\n"
                    f"📈 Entry: ${signal['entry']}\n"
                    f"🛡️ Stop Loss: ${signal['stop_loss']}\n"
                    f"🎯 Target: ${signal['target']}\n"
                    f"📊 Confidence: {confidence}\n"
                    f"💰 Simulated Capital: ${signal.get('capital', 100)} at {signal.get('leverage', 1)}x Leverage"
                )

                log_trade(signal)
                save_open_trades(open_trades)
            else:
                send_telegram_message(
                    f"⚠️ Trade rejected due to poor confidence or risk:reward ratio\n"
                    f"🪙 Pair: {signal['pair']}"
                )

        # 2. Monitor open trades
        for trade in open_trades[:]:
            if evaluate_exit_conditions(trade):
                trade["status"] = "CLOSED"
                send_telegram_message(
                    f"✅ TRADE CLOSED ({trade['direction'].upper()})\n"
                    f"🪙 Pair: {trade['pair']}\n"
                    f"📊 Entry: ${trade['entry']} | Exit: ${trade['target']}\n"
                    f"💰 PnL: Simulated"
                )
                log_trade_memory(trade)
                open_trades.remove(trade)
                save_open_trades(open_trades)

        time.sleep(TRADE_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
