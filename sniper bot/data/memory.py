# memory.py

import json
import os
from config import TRADE_MEMORY_PATH

# Ensure data file exists
def _init_memory():
    if not os.path.exists(TRADE_MEMORY_PATH):
        with open(TRADE_MEMORY_PATH, "w") as f:
            json.dump({"open": [], "closed": []}, f, indent=2)

def _load_memory():
    _init_memory()
    with open(TRADE_MEMORY_PATH, "r") as f:
        return json.load(f)

def _save_memory(data):
    with open(TRADE_MEMORY_PATH, "w") as f:
        json.dump(data, f, indent=2)

def add_open_trade(trade):
    data = _load_memory()
    data["open"].append(trade)
    _save_memory(data)

def get_open_trades():
    data = _load_memory()
    return data["open"]

def get_closed_trades():
    data = _load_memory()
    return data["closed"]

def close_trade(index, exit_price, pnl):
    data = _load_memory()
    if 0 <= index < len(data["open"]):
        trade = data["open"].pop(index)
        trade["exit_price"] = exit_price
        trade["pnl"] = pnl
        data["closed"].append(trade)
        _save_memory(data)

def overwrite_open_trades(trades):
    data = _load_memory()
    data["open"] = trades
    _save_memory(data)

def clear_all_trades():
    _save_memory({"open": [], "closed": []})
