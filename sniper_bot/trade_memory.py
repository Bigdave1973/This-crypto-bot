# trade_memory.py

import json
import os
from datetime import datetime

TRADE_LOG_FILE = "logs/trade_log.json"

def log_trade(trade_data):
    """
    Save a trade's details to the memory log.
    """
    os.makedirs("logs", exist_ok=True)

    log_entry = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "pair": trade_data.get("pair"),
        "direction": trade_data.get("direction"),
        "entry": trade_data.get("entry"),
        "stop_loss": trade_data.get("stop_loss"),
        "take_profit": trade_data.get("take_profit"),
        "confidence": trade_data.get("confidence"),
        "rr": round(trade_data.get("rr", 0), 2),
        "reason": trade_data.get("reason", "N/A"),
        "pnl": trade_data.get("pnl", 0),
        "status": trade_data.get("status", "simulated")  # could be "open", "closed", etc.
    }

    if os.path.exists(TRADE_LOG_FILE):
        with open(TRADE_LOG_FILE, "r") as f:
            existing = json.load(f)
    else:
        existing = []

    existing.append(log_entry)

    with open(TRADE_LOG_FILE, "w") as f:
        json.dump(existing, f, indent=2)

def get_trade_history():
    """
    Load all past trades from the log.
    """
    if os.path.exists(TRADE_LOG_FILE):
        with open(TRADE_LOG_FILE, "r") as f:
            return json.load(f)
    return []
