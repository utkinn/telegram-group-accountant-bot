from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from ..model.collection import Collection
from ._util import GROUP_LIKE, chat_type


@chat_type(GROUP_LIKE)
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    collection: Collection | None = context.chat_data.get("collection")
    if not collection:
        await update.effective_chat.send_message(
            f"🤔 Никакого сбора не было объявлено.\n\n/help@{context.bot.username}"
        )
        return

    formatted_spends = "\n".join(
        f"- {spend.name} ({spend.amount} ₽) — @{spend.spender_user_name}"
        for spend in collection.spends
    ) or "_Пока что никто_"

    await update.effective_chat.send_message(
        f"""Текущий сбор — *{collection.name}*
Сбор создан {collection.created_at.strftime("%d.%m.%Y")}

Кто на что потратился:
{formatted_spends}
""",
        parse_mode=ParseMode.MARKDOWN,
    )
