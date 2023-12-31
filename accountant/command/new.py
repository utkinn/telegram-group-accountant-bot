from pathlib import Path

from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ContextTypes

from ..model.collection import Collection
from ._util import chat_type


@chat_type(ChatType.GROUP)
async def new(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        collection_name = context.args[0]
    except IndexError:
        await update.effective_chat.send_message("🤔 Не понял название сбора. Попробуй ещё раз.")
        return

    context.chat_data["collection"] = Collection(collection_name)

    await update.effective_chat.send_message(
        f"""🎩 Я создал сбор с названием {collection_name}.

Добавляйте расходы таким образом:
/spend@PiuAccountantBot Ром 100

И, когда настанет время распределять, укажи всех, кто скидывается:
/count@PiuAccountantBot @foo @bar @baz"""
    )
