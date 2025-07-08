# open_trade_tracker.py

from breakeven_manager import move_sl_to_breakeven
from trade_memory import get_trade_history, log_trade
from market_reader import fetch_market_data
from telegram_alert import send_telegram_alert
import time

# Optional: could be persistent in DB later
OPEN_TRADES = []

def load_open_trades():
    global OPEN_TRADES
    OPEN_TRADES = [t for t in get_trade_history() if t["status"] == "open"]

def track_open_trades():
    global OPEN_TRADES

    if not OPEN_TRADES:
        return

    pairs = [t["pair"] for t in OPEN_TRADES]
    market_data = fetch_market_data(pairs)

    updated_trades = []
    for trade in OPEN_TRADES:
        pair = trade["pair"]
        if pair not in market_data:
            continue

        current_price = market_data[pair]["price"]
        trade["current_price"] = current_price

        # LONG Trade Check
        if trade["direction"] == "LONG":
            if current_price <= trade["stop_loss"]:
                trade["pnl"] = round((current_price - trade["entry"]), 4)
                trade["status"] = "closed"
                trade["reason"] = "SL Hit"
                send_telegram_alert(trade)
                log_trade(trade)
                continue
            elif current_price >= trade["take_profit"]:
                trade["pnl"] = round((trade["take_profit"] - trade["entry"]), 4)
                trade["status"] = "closed"
                trade["reason"] = "TP Hit"
                send_telegram_alert(trade)
                log_trade(trade)
                continue

        # SHORT Trade Check
        elif trade["direction"] == "SHORT":
            if current_price >= trade["stop_loss"]:
                trade["pnl"] = round((trade["entry"] - current_price), 4)
                trade["status"] = "closed"
                trade["reason"] = "SL Hit"
                send_telegram_alert(trade)
                log_trade(trade)
                continue
            elif current_price <= trade["take_profit"]:
                trade["pnl"] = round((trade["entry"] - trade["take_profit"]), 4)
                trade["status"] = "closed"
                trade["reason"] = "TP Hit"
                send_telegram_alert(trade)
                log_trade(trade)
                continue

        # Check for SL-to-breakeven adjustment
        if move_sl_to_breakeven(trade):
            trade["reason"] = "SL moved to breakeven"
            send_telegram_alert(trade)

        updated_trades.append(trade)

    OPEN_TRADES = updated_trades
