# trade_memory.py

import json
import os

MEMORY_FILE = "data/trade_memory.json"

def update_trade_memory(trade):
    trades = []

    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            trades = json.load(f)

    trades.append(trade)

    with open(MEMORY_FILE, "w") as f:
        json.dump(trades, f, indent=4)

def summarize_trades(limit=10):
    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as f:
        trades = json.load(f)

    return trades[-limit:]  # return last few trades
