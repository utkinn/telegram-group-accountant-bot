from pathlib import Path

from telegram import Update
from telegram.constants import ChatType, ParseMode
from telegram.ext import ContextTypes

from ..model.collection import Collection
from ._util import chat_type


@chat_type(ChatType.GROUP)
async def new(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.chat_data.get("collection"):
        await update.effective_chat.send_message(
            f"""🤔 Уже объявлен сбор *"{context.chat_data['collection'].name}"*. Рассчитай текущий сбор с помощью
            
/count@PiuAccountantBot @foo @bar @baz

либо отмени его с помощью /cancel@PiuAccountantBot""",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    collection_name = " ".join(context.args)
    if not collection_name.strip():
        await update.effective_chat.send_message(
            "🤔 Не понял название сбора. Попробуй ещё раз:\n\n/new@PiuAccountantBot название"
        )
        return

    context.chat_data["collection"] = Collection(collection_name)

    await update.effective_chat.send_message(
        f"""🎩 Я создал сбор с названием *{collection_name}*.

Ребятам, кто на что-то потратился — добавляйте расходы таким образом:
/spend@PiuAccountantBot Ром 100
*Команду вызывает только тот, кто потратился. Иначе деньги уйдут не тому человеку.*

И, в самом конце, когда настанет время распределять, один из вас должен указать, кто скидывается:
/count@PiuAccountantBot @foo @bar @baz
Сюда можно вписывать либо @меншены, либо просто имена.""",
        parse_mode=ParseMode.MARKDOWN,
    )
