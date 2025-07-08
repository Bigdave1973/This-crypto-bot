import json
import os
from datetime import datetime

TRADE_LOG_PATH = "data/trade_memory.json"

def update_trade_memory(trade):
    if not os.path.exists("data"):
        os.makedirs("data")

    memory = []
    if os.path.exists(TRADE_LOG_PATH):
        with open(TRADE_LOG_PATH, "r") as f:
            try:
                memory = json.load(f)
            except json.JSONDecodeError:
                memory = []

    memory.append(trade)

    with open(TRADE_LOG_PATH, "w") as f:
        json.dump(memory, f, indent=2)

def get_trade_history():
    if os.path.exists(TRADE_LOG_PATH):
        with open(TRADE_LOG_PATH, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def summarize_trades(limit=10):
    history = get_trade_history()
    if not history:
        return "📭 No trade history found."

    last_trades = history[-limit:]
    summary = "📈 Closed Trades (Last {}):\n".format(len(last_trades))
    for trade in last_trades:
        summary += (
            f"{trade['pair']} {trade['direction']} | "
            f"Entry: ${trade['entry']:.4f} | "
            f"Exit: ${trade.get('exit', 'N/A')} | "
            f"P/L: ${trade.get('pnl', 'N/A')}\n"
        )
    return summary

def log_trade(trade, exit_price, pnl):
    trade["exit"] = exit_price
    trade["pnl"] = pnl
    trade["closed_at"] = datetime.utcnow().isoformat()

    update_trade_memory(trade)
