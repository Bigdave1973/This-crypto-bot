# commands/closed_trades.py

from telegram import Update
from telegram.ext import CallbackContext
from memory import get_closed_trades

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

        message += (
            f"\n*{i}. {trade['pair']}* | {trade['type']}{tag}\n"
            f"Entry: ${trade.get('entry_price', 0):,.4f} | Exit: ${trade.get('exit_price', 0):,.4f}\n"
            f"PnL: `{pnl_str}` | Confidence: {trade.get('confidence', '?')}% | R:R: {trade.get('rr', '?')}\n"
        )

    update.message.reply_text(message, parse_mode="Markdown")
