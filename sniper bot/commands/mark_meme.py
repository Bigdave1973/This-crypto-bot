# commands/mark_meme.py

from telegram import Update
from telegram.ext import CallbackContext
from utils import mark_meme

def handle_mark_meme(update: Update, context: CallbackContext):
    args = context.args[1:]  # skip "mark_meme"

    if not args:
        update.message.reply_text("❗Usage: /sniper mark_meme <COIN>")
        return

    symbol = args[0].upper().replace("USDT", "")
    mark_meme(symbol)
    update.message.reply_text(f"✅ {symbol} has been marked as a *meme coin*", parse_mode="Markdown")
