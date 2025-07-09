# commands/analyze.py

from telegram import Update
from telegram.ext import CallbackContext
from trade_engine import analyze_manual_trade
from config import CHAT_ID

def handle_analyze(update: Update, context: CallbackContext, args: list):
    if not args:
        update.message.reply_text("❗Usage: /sniper analyze <PAIR>\nExample: /sniper analyze SOLUSDT")
        return

    pair = args[0].upper()

    try:
        result = analyze_manual_trade(pair)

        if result["valid"]:
            update.message.reply_text(
                f"✅ Trade Validated for {pair}\n"
                f"- Confidence: {result['confidence']}%\n"
                f"- R:R: {result['rr']}\n"
                f"- Direction: {result['direction']}\n"
                f"- Reason: {result['reason']}\n\n"
                f"💥 Simulated as 'Friend Trade' and tracking..."
            )
        else:
            update.message.reply_text(
                f"❌ Trade rejected for {pair}\n"
                f"Reason: {result['reason']}"
            )

    except Exception as e:
        update.message.reply_text(f"⚠️ Error analyzing {pair}: {e}")
