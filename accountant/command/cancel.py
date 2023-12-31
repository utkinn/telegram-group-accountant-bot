from pathlib import Path

from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ContextTypes

from ..model.collection import Collection
from ._util import chat_type


@chat_type(ChatType.GROUP)
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.chat_data.get("collection"):
        await update.effective_chat.send_message(
            f"🤔 Никакого сбора не было объявлено.\n\n/help@{context.bot.username}"
        )
        return

    context.chat_data["collection"] = None

    await update.effective_chat.send_message("👌")
