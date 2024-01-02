from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from ._util import GROUP_LIKE, chat_type


@chat_type(GROUP_LIKE)
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.chat_data.get("collection"):
        await update.effective_chat.send_message(
            f"🤔 Никакого сбора не было объявлено.\n\n/help@{context.bot.username}"
        )
        return

    context.chat_data["collection"] = None

    await update.effective_chat.send_message("👌")
