from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from ..model.collection import Collection
from ._util import GROUP_LIKE, chat_type


@chat_type(GROUP_LIKE)
async def new(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.chat_data.get("collection"):
        await update.effective_chat.send_message(
            f"""🤔 Уже объявлен сбор *"{context.chat_data['collection'].name}"*. Рассчитай текущий сбор с помощью
            
/count@{context.bot.username} @foo @bar @baz

либо отмени его с помощью /cancel@{context.bot.username}""",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    collection_name = " ".join(context.args)
    if not collection_name.strip():
        await update.effective_chat.send_message(
            f"🤔 Не понял название сбора. Попробуй ещё раз:\n\n/new@{context.bot.username} название"
        )
        return

    context.chat_data["collection"] = Collection(collection_name)

    await update.effective_chat.send_message(
        f"""🎩 Я создал сбор с названием *{collection_name}*.

Ребятам, кто на что-то потратился — добавляйте расходы таким образом:
/spend@{context.bot.username} Ром 100
*Команду вызывает только тот, кто потратился. Иначе деньги уйдут не тому человеку.*

И, в самом конце, когда все расходы занесены и настанет время распределять, один из вас должен указать, кто скидывается:
/count@{context.bot.username} @foo @bar @baz
Сюда можно вписывать либо @меншены, либо просто имена.""",
        parse_mode=ParseMode.MARKDOWN,
    )
