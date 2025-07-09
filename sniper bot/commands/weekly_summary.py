# commands/weekly_summary.py

from telegram import Update
from telegram.ext import CallbackContext
from memory import get_closed_trades
from datetime import datetime, timedelta

def handle_weekly_summary(update: Update, context: CallbackContext):
    trades = get_closed_trades()

    if not trades:
        update.message.reply_text("📭 No closed trades to summarize.")
        return

    one_week_ago = datetime.now() - timedelta(days=7)

    recent_trades = []
    for trade in trades:
        t_str = trade.get("timestamp") or trade.get("time")
        if not t_str:
            continue
        try:
            t = datetime.fromisoformat(t_str)
            if t >= one_week_ago:
                recent_trades.append(trade)
        except:
            continue

    if not recent_trades:
        update.message.reply_text("📭 No trades closed in the last 7 days.")
        return

    wins = [t for t in recent_trades if t.get("pnl", 0) > 0]
    avg_pnl = round(sum(t.get("pnl", 0) for t in recent_trades) / len(recent_trades), 2)
    avg_conf = round(sum(t.get("confidence", 0) for t in recent_trades) / len(recent_trades), 2)
    avg_rr = round(sum(t.get("rr", 0) for t in recent_trades) / len(recent_trades), 2)
    win_rate = round((len(wins) / len(recent_trades)) * 100, 2)

    msg = (
        "🗓️ *Weekly Sniper Summary (7d)*\n"
        f"- Trades: {len(recent_trades)}\n"
        f"- Win Rate: {win_rate}%\n"
        f"- Avg PnL: ${avg_pnl}\n"
        f"- Avg Confidence: {avg_conf}%\n"
        f"- Avg R:R: {avg_rr}"
    )

    update.message.reply_text(msg, parse_mode="Markdown")
