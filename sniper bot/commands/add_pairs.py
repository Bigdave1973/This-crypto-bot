# commands/add_pair.py

from telegram import Update
from telegram.ext import CallbackContext
from pairs import add_pair

def handle_add_pair(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage: /sniper add_pair <SYMBOL>")
        return

    pair = context.args[0].upper()
    if add_pair(pair):
        update.message.reply_text(f"✅ Added pair: {pair}")
    else:
        update.message.reply_text(f"⚠️ Pair already exists: {pair}")
