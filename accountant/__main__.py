import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from .command.help import help


def main():
    load_dotenv()
    token = get_token()

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("help", help))
    app.run_polling()


def get_token():
    token = os.getenv("TOKEN")
    if not token:
        print("TOKEN not set. Check .env file.")
        exit(1)
    return token


main()
