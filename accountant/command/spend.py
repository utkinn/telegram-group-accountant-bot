import re
from datetime import datetime

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from ..model.collection import Collection, Spend
from ._util import GROUP_LIKE, chat_type


@chat_type(GROUP_LIKE)
async def spend(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        args_without_mentions = re.sub(r"@\w+", "", " ".join(context.args)).split()
        (*item_name, price) = args_without_mentions
        item_name = " ".join(item_name)
        price = int(price)
    except IndexError:
        await update.effective_chat.send_message(
            f"🤔 Не понял, что ты купил. Попробуй ещё раз.\n\n/help@{context.bot.username}"
        )
        return
    except ValueError:
        await update.effective_chat.send_message(
            f"🤔 Не понял, сколько это стоило. Попробуй ещё раз.\n\n/help@{context.bot.username}"
        )
        return
    if price < 0:
        await update.effective_chat.send_message(
            f"🤔 Не понял, сколько это стоило. Попробуй ещё раз.\n\n/help@{context.bot.username}"
        )
        return

    mentions = re.findall(r"@\w+", " ".join(context.args))
    if len(mentions) > 1:
        await update.effective_chat.send_message(
            "🤔 Можно указать лишь одного потратившегося."
        )
        return

    collection_just_created = False
    if not context.chat_data.get("collection"):
        collection_just_created = True
        collection_name = datetime.now().strftime("%d.%m.%Y")
        context.chat_data["collection"] = Collection(collection_name)

    collection: Collection = context.chat_data["collection"]
    context.chat_data["collection"] = collection.with_new_spend(
        Spend(item_name, price, update.effective_user.username if not mentions else mentions[0].lstrip("@"))
    )

    whose_spend = "твою трату" if not mentions else f"трату {mentions[0]}"

    await update.effective_chat.send_message(
        f"✍️ Занес {whose_spend} на {item_name} за {price} ₽."
        + (
            f"""\n\nСбор не был объявлен. Я создал его за тебя и назвал его "{collection.name}". Можешь дать ему название командой "/rename@{context.bot.username} название".
            
*Ребятам, кто на что-то потратился* — добавляйте расходы таким образом:
/spend@{context.bot.username} Ром 100
*Команду вызывает только тот, кто потратился. Иначе деньги уйдут не тому человеку.*

И, в самом конце, когда настанет время распределять, один из вас должен указать, кто скидывается:
/count@{context.bot.username} @foo @bar @baz
Сюда можно вписывать либо @меншены, либо просто имена."""
            if collection_just_created
            else ""
        ),
        parse_mode=ParseMode.MARKDOWN,
    )
