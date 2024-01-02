from telegram import Update
from telegram.ext import ContextTypes

from ._util import GROUP_LIKE, chat_type


@chat_type(GROUP_LIKE)
async def rename(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    new_name = " ".join(context.args)
    if not new_name.strip():
        await update.effective_chat.send_message(
            "🤔 Не понял название сбора. Попробуй ещё раз."
        )
        return

    if not context.chat_data.get("collection"):
        await update.effective_chat.send_message(
            f"🤔 Никакого сбора не было объявлено.\n\n/help@{context.bot.username}"
        )
        return

    context.chat_data["collection"] = context.chat_data["collection"].renamed(new_name)

    await update.effective_chat.send_message("👌")
