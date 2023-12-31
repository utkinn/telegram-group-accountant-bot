import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, PicklePersistence

from .command.help import help
from .command.new import new


def main():
    load_dotenv()
    token = get_token()

    app = (
        ApplicationBuilder()
        .token(token)
        .persistence(PicklePersistence(get_persistence_file_path()))
        .build()
    )
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("new", new))
    app.run_polling()


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
