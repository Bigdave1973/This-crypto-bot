import time
from utils.memory import load_open_trades, update_trade_exit
from utils.telegram import send_trade_exit_alert

def check_open_trades():
    trades = load_open_trades()
    for trade in trades:
        if time.time() - trade['timestamp'] > 30:
            pnl = (trade['entry_price'] * 0.98) - trade['entry_price']
            update_trade_exit(trade['pair'], trade['entry_price'] * 0.98, "TP Hit", pnl)
            send_trade_exit_alert(trade['pair'], trade['entry_price'] * 0.98, "TP Hit", pnl)
