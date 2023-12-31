import os
import asyncio
import telegram
from dotenv import load_dotenv


async def main():
    load_dotenv()
    token = os.getenv("TOKEN")
    if not token:
        print("TOKEN not set. Check .env file.")
        exit(1)

    bot = telegram.Bot(token)
    async with bot:
        print(await bot.get_me())


asyncio.run(main())
