from math import floor

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from ..model.collection import Collection, Invoice
from ._util import GROUP_LIKE, chat_type


@chat_type(GROUP_LIKE)
async def count(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.effective_chat.send_message(
            f"🤔 Не понял, кто скидывается. Попробуй ещё раз.\n\n/help@{context.bot.username}"
        )
        return

    collection: Collection | None = context.chat_data.get("collection")
    if not collection:
        await update.effective_chat.send_message(
            f"""🤔 Никакого сбора не было объявлено. Создайте сбор командой:
/new@{context.bot.username} название

и пригласите участников заносить свои траты командой
/spend@{context.bot.username} название траты 100

либо занесите за них командой
/spend@{context.bot.username} название траты 100 @SpenderUserName

Справка: /help@{context.bot.username}""",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if not collection.spends:
        await update.effective_chat.send_message(
            f"""🤔 Не занесено ни одной траты.
            
*Всем, кто потратился на {collection.name}:*
Занесите свои траты с помощью команды:

/spend@{context.bot.username} Название траты 100

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
    formatted_payees = _format_payees(context, invoices, context.bot_data)

    if "last_count_message_id" in context.chat_data:
        await context.bot.delete_message(
            update.effective_chat.id, context.chat_data["last_count_message_id"]
        )

    message = await update.effective_chat.send_message(
        f"""<b>🤑 Настал час расплаты за {collection.name}!</b>
<i>Дамы и господа, подайте кто-нибудь. Кто сколько может. 🎩</i>
Сбор создан {collection.created_at.strftime("%d.%m.%Y")}

Кто на что потратился:
{formatted_spends}

Кто переводит:
{formatted_payers}

Кому сколько перевести:
{formatted_payees}

<i>Перепроверьте, что все расходы занесены и все участники сбора указаны.</i>
<i>Если все в порядке, закройте сбор командой</i>\n/cancel@{context.bot.username}.
<i>Если затесался неправильный расход, уберите его командой\n/unspend@{context.bot.username} номер_расхода_в_команде_info\n
Потом занесите правильный и вызовите /count@{context.bot.username} еще раз.</i>""",
        parse_mode=ParseMode.HTML,
    )
    context.chat_data["last_count_message_id"] = message.id


def _format_payees(
    context: ContextTypes.DEFAULT_TYPE, invoices: list[Invoice], bot_data: dict
):
    result = "\n".join(_format_payee(invoice, context.bot_data) for invoice in invoices)
    payee_user_names = list(
        sorted(set(invoice.payee_user_name for invoice in invoices))
    )
    payee_user_names_without_requisites = [
        username
        for username in payee_user_names
        if not bot_data.get("requisites", {}).get(username)
    ]
    if payee_user_names_without_requisites:
        result += (
            "\n\n👋 "
            + ", ".join(
                "@" + username for username in payee_user_names_without_requisites
            )
            + ", предлагаю сходить ко мне в личку и указать реквизиты, куда переводить тебе деньги. Так будет удобнее 😉"
        )
    return result


def _format_payee(invoice: Invoice, bot_data: dict) -> str:
    result = f"- Подайте @{invoice.payee_user_name} по {floor(invoice.amount)} ₽"
    requisite = bot_data.get("requisites", {}).get(invoice.payee_user_name)
    bank = bot_data.get("preferred_banks", {}).get(invoice.payee_user_name)
    if requisite or bank:
        result += " (" + ", ".join(filter(None, [requisite, bank])) + ")"
    return result
