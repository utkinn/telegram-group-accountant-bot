import os

from dotenv import load_dotenv
from telegram import BotCommandScopeAllGroupChats, BotCommandScopeAllPrivateChats
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    PicklePersistence,
)

from .command import group_descriptions as group_command_descriptions
from .command import private_descriptions as private_command_descriptions
from .command.cancel import cancel
from .command.count import count
from .command.help import help
from .command.info import info
from .command.new import new
from .command.rename import rename
from .command.requisites import conv_handler as requisites_conv_handler
from .command.spend import spend
from .command.start import start
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
    app.add_handlers(
        [
            CommandHandler("help", help),
            CommandHandler("new", new),
            CommandHandler("count", count),
            CommandHandler("info", info),
            CommandHandler("rename", rename),
            CommandHandler("spend", spend),
            CommandHandler("unspend", unspend),
            CommandHandler("cancel", cancel),
            CommandHandler("start", start),
            requisites_conv_handler,
        ]
    )
    app.run_polling()


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        group_command_descriptions.items(), BotCommandScopeAllGroupChats()
    )
    await application.bot.set_my_commands(
        private_command_descriptions.items(), BotCommandScopeAllPrivateChats()
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
