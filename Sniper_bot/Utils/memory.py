import json, os, time

MEMORY_FILE = "data/trade_memory.json"
OPEN_TRADES_FILE = "data/open_trades.json"

def _load(filepath):
    if not os.path.exists(filepath): return []
    with open(filepath, 'r') as f:
        try: return json.load(f)
        except: return []

def _save(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def save_open_trade(trade):
    trades = _load(OPEN_TRADES_FILE)
    trades.append(trade)
    _save(OPEN_TRADES_FILE, trades)

def update_trade_exit(pair, exit_price, result, pnl):
    trades = _load(OPEN_TRADES_FILE)
    for t in trades:
        if t["pair"] == pair:
            trades.remove(t)
            t["exit_price"] = exit_price
            t["result"] = result
            t["pnl"] = pnl
            t["exit_time"] = time.time()
            save_trade_to_memory(t)
            break
    _save(OPEN_TRADES_FILE, trades)

def save_trade_to_memory(trade):
    mem = _load(MEMORY_FILE)
    mem.append(trade)
    _save(MEMORY_FILE, mem)

def load_open_trades():
    return _load(OPEN_TRADES_FILE)
