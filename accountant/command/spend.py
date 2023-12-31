from datetime import datetime

from telegram import Update
from telegram.constants import ChatType, ParseMode
from telegram.ext import ContextTypes

from ..model.collection import Collection, Spend
from ._util import chat_type


@chat_type(ChatType.GROUP)
async def spend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        (*item_name, price) = context.args
        item_name = " ".join(item_name)
        price = int(price)
    except IndexError:
        await update.effective_chat.send_message(
            "🤔 Не понял, что ты купил. Попробуй ещё раз.\n\n/help@PiuAccountantBot"
        )
        return
    except ValueError:
        await update.effective_chat.send_message(
            "🤔 Не понял, сколько это стоило. Попробуй ещё раз.\n\n/help@PiuAccountantBot"
        )
        return
    if price < 0:
        await update.effective_chat.send_message(
            "🤔 Не понял, сколько это стоило. Попробуй ещё раз.\n\n/help@PiuAccountantBot"
        )
        return

    collection_just_created = False
    if not context.chat_data.get("collection"):
        collection_just_created = True
        collection_name = datetime.now().strftime("%d.%m.%Y")
        context.chat_data["collection"] = Collection(collection_name)

    collection: Collection = context.chat_data["collection"]
    context.chat_data["collection"] = collection.with_new_spend(
        Spend(item_name, price, update.effective_user.username)
    )

    await update.effective_chat.send_message(
        f"✍️ Занес твою трату на {item_name} за {price} ₽."
        + (
            f"""\n\nСбор не был объявлен. Я создал его за тебя и назвал его "{collection.name}". Можешь дать ему название командой "/rename@PiuAccountantBot название".
            
*Ребятам, кто на что-то потратился* — добавляйте расходы таким образом:
/spend@PiuAccountantBot Ром 100
*Команду вызывает только тот, кто потратился. Иначе деньги уйдут не тому человеку.*

И, в самом конце, когда настанет время распределять, один из вас должен указать, кто скидывается:
/count@PiuAccountantBot @foo @bar @baz
Сюда можно вписывать либо @меншены, либо просто имена."""
            if collection_just_created
            else ""
        ),
        parse_mode=ParseMode.MARKDOWN,
    )
