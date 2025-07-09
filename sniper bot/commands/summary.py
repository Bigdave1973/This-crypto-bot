# commands/summary.py

from telegram import Update
from telegram.ext import CallbackContext
from memory import get_closed_trades

def handle_summary(update: Update, context: CallbackContext):
    trades = get_closed_trades()

    if not trades:
        update.message.reply_text("📭 No closed trades yet. No stats to show.")
        return

    wins = [t for t in trades if t.get("pnl", 0) > 0]
    losses = [t for t in trades if t.get("pnl", 0) <= 0]

    win_rate = round((len(wins) / len(trades)) * 100, 2)
    avg_pnl = round(sum(t.get("pnl", 0) for t in trades) / len(trades), 2)
    avg_conf = round(sum(t.get("confidence", 0) for t in trades) / len(trades), 2)
    avg_rr = round(sum(t.get("rr", 0) for t in trades) / len(trades), 2)

    msg = (
        "📈 *Sniper Performance Summary:*\n"
        f"- Total Trades: {len(trades)}\n"
        f"- Win Rate: {win_rate}%\n"
        f"- Avg PnL: ${avg_pnl}\n"
        f"- Avg Confidence: {avg_conf}%\n"
        f"- Avg R:R: {avg_rr}"
    )

    update.message.reply_text(msg, parse_mode="Markdown")
