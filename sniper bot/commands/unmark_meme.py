# commands/unmark_meme.py

from telegram import Update
from telegram.ext import CallbackContext
from utils import unmark_meme

def handle_unmark_meme(update: Update, context: CallbackContext):
    args = context.args[1:]  # skip "unmark_meme"

    if not args:
        update.message.reply_text("❗Usage: /sniper unmark_meme <COIN>")
        return

    symbol = args[0].upper().replace("USDT", "")
    unmark_meme(symbol)
    update.message.reply_text(f"✅ {symbol} has been removed from *meme coin* status", parse_mode="Markdown")
