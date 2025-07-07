import os
import json
from datetime import datetime

LOG_FILE = "memory/trade_log.json"

def log_trade(trade):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "trade": trade
    }
    append_log(entry)

def log_trade_memory(trade):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "status": "CLOSED",
        "trade": trade
    }
    append_log(entry)

def append_log(entry):
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([entry], f, indent=4)
    else:
        with open(LOG_FILE, "r+") as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=4)
