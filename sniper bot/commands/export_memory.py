# commands/export_memory.py

from telegram import Update
from telegram.ext import CallbackContext
from config import TRADE_MEMORY_PATH

def handle_export_memory(update: Update, context: CallbackContext):
    try:
        with open(TRADE_MEMORY_PATH, "rb") as f:
            update.message.reply_document(document=f, filename="trade_memory.json")
    except Exception as e:
        update.message.reply_text(f"❌ Failed to send memory file: {e}")
