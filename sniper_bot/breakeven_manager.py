# breakeven_manager.py

def move_sl_to_breakeven(trade):
    """
    Adjust SL to breakeven if TP1 has been hit.
    """
    if not trade.get("sl_moved") and trade.get("status") == "open":
        entry = trade["entry"]
        tp1 = trade["take_profit"]
        current_price = trade.get("current_price")

        if trade["direction"] == "LONG" and current_price >= tp1:
            trade["stop_loss"] = entry
            trade["sl_moved"] = True
            return True

        elif trade["direction"] == "SHORT" and current_price <= tp1:
            trade["stop_loss"] = entry
            trade["sl_moved"] = True
            return True

    return False
