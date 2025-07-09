# commands/remove_pair.py

from telegram import Update
from telegram.ext import CallbackContext
from pairs import remove_pair

def handle_remove_pair(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage: /sniper remove_pair <SYMBOL>")
        return

    pair = context.args[0].upper()
    if remove_pair(pair):
        update.message.reply_text(f"❌ Removed pair: {pair}")
    else:
        update.message.reply_text(f"⚠️ Pair not found: {pair}")
