from math import floor

from telegram import Update
from telegram.constants import ChatType, ParseMode
from telegram.ext import ContextTypes

from ..model.collection import Collection
from ._util import chat_type


@chat_type(ChatType.GROUP)
async def count(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.effective_chat.send_message(
            "🤔 Не понял, кто скидывается. Попробуй ещё раз.\n\n/help@PiuAccountantBot"
        )
        return

    collection: Collection | None = context.chat_data.get("collection")
    if not collection:
        await update.effective_chat.send_message(
            """🤔 Никакого сбора не было объявлено. Создайте сбор командой:
/new@PiuAccountantBot название

и пригласите участников заносить свои траты командой /spend@PiuAccountantBot название траты 100
*Команду /spend вызывает только тот, кто потратил деньги на что-то! Иначе они зачтутся не тому человеку!*

Справка: /help@PiuAccountantBot""",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if not collection.spends:
        await update.effective_chat.send_message(
            f"""🤔 Не занесено ни одной траты.
            
*Всем, кто потратился на {collection.name}:*
Занесите свои траты с помощью команды:

/spend@PiuAccountantBot Название траты 100

где 100 — сумма в рублях.
""",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    invoices = collection.spread(len(context.args))

    formatted_spends = "\n".join(
        f"{n}. {spend.name} ({spend.amount} ₽) — @{spend.spender_user_name}"
        for (n, spend) in enumerate(collection.spends, start=1)
    )
    payers = list(sorted(set(context.args)))
    formatted_payers = "\n".join(f"- {user_name}" for user_name in payers)
    formatted_payees = "\n".join(
        f"- Подайте @{invoice.payee_user_name} по {floor(invoice.amount)} ₽"
        for invoice in invoices
    )

    # TODO: requisites
    await update.effective_chat.send_message(
        f"""*🤑 Настал час расплаты за {collection.name}!*
_Дамы и господа, подайте кто-нибудь. Кто сколько может. 🎩_
Сбор создан {collection.created_at.strftime("%d.%m.%Y")}

Кто на что потратился:
{formatted_spends}

Кто переводит:
{formatted_payers}

Кому сколько перевести:
{formatted_payees}

_Перепроверьте, что все расходы занесены и все участники сбора указаны._
_Если все в порядке, закройте сбор командой_\n/cancel@PiuAccountantBot.
_Если затесался неправильный расход, уберите его командой /unspend@PiuAccountantBot <номер>._""",
        parse_mode=ParseMode.MARKDOWN,
    )
