# commands/list_pairs.py

from telegram import Update
from telegram.ext import CallbackContext
from pairs import load_pairs

def handle_list_pairs(update: Update, context: CallbackContext):
    pairs = load_pairs()
    if not pairs:
        update.message.reply_text("📭 No trading pairs are currently tracked.")
        return

    text = "\n".join([f"- {p}" for p in pairs])
    update.message.reply_text(f"📊 *Active Pairs:* \n{text}", parse_mode="Markdown")
