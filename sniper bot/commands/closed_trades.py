# commands/closed_trades.py

from telegram import Update
from telegram.ext import CallbackContext
from memory import get_closed_trades
from datetime import datetime

def format_duration(start_str, end_str):
    try:
        start = datetime.fromisoformat(start_str)
        end = datetime.fromisoformat(end_str)
        delta = end - start
        hours, minutes = divmod(delta.seconds, 3600)[0], (delta.seconds % 3600) // 60
        if delta.days:
            return f"{delta.days}d {hours}h {minutes}m"
        return f"{hours}h {minutes}m"
    except:
        return "unknown"

def handle_closed_trades(update: Update, context: CallbackContext):
    trades = get_closed_trades()

    if not trades:
        update.message.reply_text("📭 No closed trades found.")
        return

    message = f"📈 *Closed Trades* (Last {min(len(trades), 10)})\n"

    for i, trade in enumerate(trades[-10:], start=1):
        pnl = trade.get("pnl", 0)
        pnl_str = f"+${pnl:.2f}" if pnl >= 0 else f"-${abs(pnl):.2f}"
        tag = " | Friend Trade" if trade.get("friend_trade") else ""

        duration = format_duration(trade.get("timestamp", ""), trade.get("closed_at", ""))

        message += (
            f"\n*{i}. {trade['pair']}* | {trade['type']}{tag}\n"
            f"Entry: ${trade.get('entry_price', 0):,.4f} | Exit: ${trade.get('exit_price', 0):,.4f}\n"
            f"PnL: `{pnl_str}` | Duration: {duration} | Confidence: {trade.get('confidence', '?')}% | R:R: {trade.get('rr', '?')}\n"
        )

    update.message.reply_text(message, parse_mode="Markdown")
