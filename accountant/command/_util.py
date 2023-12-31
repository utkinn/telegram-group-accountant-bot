from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ContextTypes


def chat_type(chat_type: ChatType):
    def decorator(handler):
        async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            if update.effective_chat.type != chat_type:
                return

            await handler(update, context)

        return wrapped

    return decorator
