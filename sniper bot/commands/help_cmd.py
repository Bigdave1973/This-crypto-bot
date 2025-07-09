# commands/help_cmd.py

from telegram import Update
from telegram.ext import CallbackContext

def handle_help(update: Update, context: CallbackContext):
    help_text = (
        "📖 *Sniper Bot Commands:*\n"
        "/sniper analyze <PAIR> — Analyze and simulate a trade\n"
        "/sniper open_trades — View all active trades\n"
        "/sniper closed_trades — View past closed trades\n"
        "/sniper config — View or update bot settings\n"
        "/sniper add_pair <PAIR> — Add a trading pair\n"
        "/sniper remove_pair <PAIR> — Remove a trading pair\n"
        "/sniper list_pairs — List all active pairs\n"
        "/sniper summary — Stats on win rate, avg PnL, R:R\n"
        "/sniper export_memory — Download all saved trade data\n"
        "/sniper weekly_summary — Show last 7 days stats\n"
        "/ping — Check if the bot is scanning\n"
    )
    update.message.reply_text(help_text, parse_mode="Markdown")
