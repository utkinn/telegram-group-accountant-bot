from pathlib import Path

from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ContextTypes

from ._util import chat_type


@chat_type(ChatType.PRIVATE)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open(Path(__file__).parent / "start.md") as f:
        await update.effective_chat.send_message(f.read().replace("BOT_NAME", context.bot.first_name))
