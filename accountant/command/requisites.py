import re

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.constants import ChatType
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    if update.effective_chat.type != ChatType.PRIVATE:
        return ConversationHandler.END

    await update.effective_chat.send_message(
        "Напиши твой номер телефона или номер карты.",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Отправить номер телефона", request_contact=True)]],
            one_time_keyboard=True,
        ),
    )
    return "REQUISITES"


_INPUT_REGEX = re.compile(r"^(\+7|8)(\d| ){10}$|^(\d| ){16}$")


async def get_requisites(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    if update.message.text:
        inp = update.message.text.replace(" ", "")
    else:
        inp = "+" + update.message.contact.phone_number
    if not _INPUT_REGEX.match(inp):
        await update.effective_chat.send_message(
            "Неверные реквизиты. Попробуй ещё раз."
        )
        return "REQUISITES"

    if "requisites" not in context.bot_data:
        context.bot_data["requisites"] = {}
    context.bot_data["requisites"][update.effective_user.username] = inp  # TODO: create dict

    is_phone_number = len(inp) != 16
    if is_phone_number:
        await update.effective_chat.send_message("Какой банк предпочтителен?")
        return "BANK"

    await update.effective_chat.send_message(
        "Благодарю!\nЯ буду указывать твои реквизиты при распределении денег."
    )
    return ConversationHandler.END


async def bank(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    if "preferred_banks" not in context.bot_data:
        context.bot_data["preferred_banks"] = {}
    context.bot_data["preferred_banks"][update.effective_user.username] = update.message.text
    await update.effective_chat.send_message(
        "Благодарю!\nЯ буду указывать твои реквизиты при распределении денег."
    )
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("requisites", ask)],
    states={
        "REQUISITES": [
            MessageHandler(
                filters.TEXT | filters.CONTACT,
                get_requisites,
            ),
        ],
        "BANK": [MessageHandler(filters.TEXT, bank)],
    },
    fallbacks=[],
)
