from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from ._util import GROUP_LIKE, chat_type


@chat_type(GROUP_LIKE)
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open(Path(__file__).parent / "help.md") as f:
        help_text = f.read().replace("BOT_NAME", context.bot.first_name).replace("BOT_USER_NAME", context.bot.username)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=help_text,
    )
