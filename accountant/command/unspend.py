from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ContextTypes

from ..model.collection import Collection
from ._util import chat_type


@chat_type(ChatType.GROUP)
async def unspend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    collection: Collection | None = context.chat_data.get("collection")
    if not collection:
        await update.effective_chat.send_message(
            f"🤔 Никакого сбора не было объявлено.\n\n/help@{context.bot.username}"
        )
        return

    if not collection.spends:
        await update.effective_chat.send_message("🤔 Не занесено ни одной траты.")
        return

    try:
        spend_num = context.args[0]
    except (IndexError, ValueError):
        formatted_spends = "\n".join(
            f"1. {spend.name} ({spend.amount} ₽) — @{spend.spender_user_name}"
            for spend in collection.spends
        )
        await update.effective_chat.send_message(
            f"{formatted_spends}\n\nВызовите /unspend@{context.bot.username} номер_траты для удаления нужной траты."
        )
        return

    try:
        spend = collection.spends[int(spend_num) - 1]
        context.chat_data["collection"] = collection.without_spend(int(spend_num) - 1)
    except IndexError:
        await update.effective_chat.send_message(
            f"🤔 Нет траты с номером {spend_num}."
        )
        return
    
    await update.effective_chat.send_message(f"✅ Трата \"{spend.name}\" от @{spend.spender_user_name} за {spend.amount} ₽ удалена.")
