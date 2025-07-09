# commands/open_trades.py

from telegram import Update
from telegram.ext import CallbackContext
from memory import get_open_trades

def handle_open_trades(update: Update, context: CallbackContext):
    trades = get_open_trades()

    if not trades:
        update.message.reply_text("📭 No open trades at the moment.")
        return

    message = f"📊 *Open Trades* ({len(trades)})\n"

    for i, trade in enumerate(trades, start=1):
        tag = " | Friend Trade" if trade.get("friend_trade") else ""
        message += (
            f"\n*{i}. {trade['pair']}* | {trade['type']} | R:R {trade['rr']} | Confidence: {trade['confidence']}%\n"
            f"_Reason: {trade['reason']}_{tag}\n"
        )

    update.message.reply_text(message, parse_mode="Markdown")
