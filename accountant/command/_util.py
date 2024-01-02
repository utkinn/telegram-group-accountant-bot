from collections.abc import Iterable

from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ContextTypes

GROUP_LIKE = [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]


def chat_type(chat_type: ChatType | Iterable[ChatType]):
    def decorator(handler):
        async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            if isinstance(chat_type, ChatType) and update.effective_chat.type != chat_type:
                return
            if update.effective_chat.type not in chat_type:
                return

            await handler(update, context)

        return wrapped

    return decorator
