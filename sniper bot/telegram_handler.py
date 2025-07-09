from telegram import Update
from telegram.ext import CallbackContext

from commands.analyze import handle_analyze
from commands.open_trades import handle_open_trades
from commands.closed_trades import handle_closed_trades
from commands.config_cmd import handle_config
from commands.summary import handle_summary
from commands.help_cmd import handle_help
from commands.export_memory import handle_export_memory
from commands.weekly_summary import handle_weekly_summary
from commands.add_pair import handle_add_pair
from commands.remove_pair import handle_remove_pair
from commands.list_pairs import handle_list_pairs
from commands.mark_meme import handle_mark_meme
from commands.unmark_meme import handle_unmark_meme

def handle_sniper_command(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("⚠️ Please provide a subcommand. Example:\n/sniper analyze BTCUSDT")
        return

    subcommand = context.args[0].lower()
    args = context.args[1:]

    if subcommand == "analyze":
        handle_analyze(update, context, args)

    elif subcommand == "open_trades":
        handle_open_trades(update, context)

    elif subcommand == "closed_trades":
        handle_closed_trades(update, context)

    elif subcommand == "config":
        handle_config(update, context)

    elif subcommand == "summary":
        handle_summary(update, context)

    elif subcommand == "help":
        handle_help(update, context)

    elif subcommand == "export_memory":
        handle_export_memory(update, context)

    elif subcommand == "weekly_summary":
        handle_weekly_summary(update, context)

    elif subcommand == "add_pair":
        handle_add_pair(update, context)

    elif subcommand == "remove_pair":
        handle_remove_pair(update, context)

    elif subcommand == "list_pairs":
        handle_list_pairs(update, context)

    elif subcommand == "mark_meme":
        handle_mark_meme(update, context)

    elif subcommand == "unmark_meme":
        handle_unmark_meme(update, context)

    else:
        update.message.reply_text(
            f"❌ Unknown subcommand: `{subcommand}`.\nTry /sniper help",
            parse_mode="Markdown"
        )
