# commands/open_trades.py

from telegram import Update
from telegram.ext import CallbackContext
from memory import get_open_trades
from datetime import datetime

def format_time_open(timestamp):
    try:
        start = datetime.fromisoformat(timestamp)
        delta = datetime.now() - start
        hours, minutes = divmod(delta.seconds, 3600)[0], (delta.seconds % 3600) // 60
        if delta.days:
            return f"{delta.days}d {hours}h {minutes}m ago"
        return f"{hours}h {minutes}m ago"
    except:
        return "unknown"

def handle_open_trades(update: Update, context: CallbackContext):
    trades = get_open_trades()

    if not trades:
        update.message.reply_text("📭 No open trades at the moment.")
        return

    message = f"📊 *Open Trades* ({len(trades)})\n"

    for i, trade in enumerate(trades, start=1):
        tag = " | Friend Trade" if trade.get("friend_trade") else ""
        entry = trade.get("entry_price", "0.0000")
        opened = format_time_open(trade.get("timestamp", ""))

        message += (
            f"\n*{i}. {trade['pair']}* | {trade['type']} | R:R {trade['rr']} | Confidence: {trade['confidence']}%\n"
            f"Entry: ${entry} | Opened: {opened}\n"
            f"_Reason: {trade['reason']}_{tag}\n"
        )

    update.message.reply_text(message, parse_mode="Markdown")
