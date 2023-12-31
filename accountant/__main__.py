import os

from dotenv import load_dotenv
from telegram import BotCommandScopeAllGroupChats
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    PicklePersistence,
)

from .command import descriptions as command_descriptions
from .command.cancel import cancel
from .command.count import count
from .command.help import help
from .command.info import info
from .command.new import new
from .command.rename import rename
from .command.spend import spend
from .command.unspend import unspend


def main():
    load_dotenv()
    token = get_token()

    app = (
        ApplicationBuilder()
        .token(token)
        .persistence(PicklePersistence(get_persistence_file_path()))
        .post_init(post_init)
        .build()
    )
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("new", new))
    app.add_handler(CommandHandler("count", count))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("rename", rename))
    app.add_handler(CommandHandler("spend", spend))
    app.add_handler(CommandHandler("unspend", unspend))
    app.add_handler(CommandHandler("cancel", cancel))
    app.run_polling()


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        command_descriptions.items(), BotCommandScopeAllGroupChats()
    )


def get_token():
    token = os.getenv("TOKEN")
    if not token:
        print("TOKEN not set. Check .env file.")
        exit(1)
    return token


def get_persistence_file_path():
    persistence_file_path = os.getenv("PERSISTENCE_FILE_PATH")
    if not persistence_file_path:
        print("PERSISTENCE_FILE_PATH not set. Check .env file.")
        exit(1)
    return persistence_file_path


main()
