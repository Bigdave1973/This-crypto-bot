# commands/config_cmd.py

from telegram import Update
from telegram.ext import CallbackContext
import config

def handle_config(update: Update, context: CallbackContext):
    if not context.args:
        # Show current config
        msg = (
            "⚙️ *Current Sniper Config:*\n"
            f"- Capital per trade: ${config.DEFAULT_CAPITAL}\n"
            f"- Leverage: {config.DEFAULT_LEVERAGE}x\n"
            f"- Slippage: {config.SLIPPAGE_PERCENT}%\n"
            f"- Trailing SL trigger: {config.TRAILING_STOP_TRIGGER}%\n"
        )
        update.message.reply_text(msg, parse_mode="Markdown")
        return

    # Modify config values (live edit)
    key = context.args[0].lower()
    try:
        value = float(context.args[1])

        if key == "capital":
            config.DEFAULT_CAPITAL = value
        elif key == "leverage":
            config.DEFAULT_LEVERAGE = value
        elif key == "slippage":
            config.SLIPPAGE_PERCENT = value
        elif key == "trailing":
            config.TRAILING_STOP_TRIGGER = value
        else:
            update.message.reply_text("❌ Invalid config key. Use: capital, leverage, slippage, trailing")
            return

        update.message.reply_text(f"✅ Updated `{key}` to `{value}`", parse_mode="Markdown")

    except (IndexError, ValueError):
        update.message.reply_text("⚠️ Usage:\n/sniper config <key> <value>\nExample: /sniper config capital 150")
