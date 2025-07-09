import time
import threading
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from config import BOT_TOKEN, CHAT_ID
from telegram_handler import handle_sniper_command
from trade_engine import analyze_live_market

# Initialize bot
bot = Bot(token=BOT_TOKEN)

# Telegram command: /ping
def ping(update: Update, context: CallbackContext):
    update.message.reply_text("🔍 Sniper Bot is online and scanning the market...")

# Telegram command: /sniper
def sniper_handler(update: Update, context: CallbackContext):
    handle_sniper_command(update, context)

# Background thread to scan market
def market_scanner():
    while True:
        try:
            analyze_live_market(bot)
        except Exception as e:
            print(f"[Scanner Error] {e}")
        time.sleep(60)  # scan every 1 minute

def main():
    print("🚀 Sniper Bot starting...")
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register Telegram commands
    dispatcher.add_handler(CommandHandler("ping", ping))
    dispatcher.add_handler(CommandHandler("sniper", sniper_handler))

    # Start market scanner thread
    scanner_thread = threading.Thread(target=market_scanner)
    scanner_thread.daemon = True
    scanner_thread.start()

    # Start Telegram bot polling
    updater.start_polling()
    print("✅ Bot is live and scanning...")

    updater.idle()

if __name__ == "__main__":
    main()
