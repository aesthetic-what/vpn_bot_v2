from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers.handlers import router
from handlers.db.db_core import init_db
from handlers.scheduler import start_scheduler
from logger import Logger

import asyncio
import os

logger = Logger.getinstance()
load_dotenv()
token = os.getenv("TELEGRAM_TOKEN")

async def main():
    await init_db()
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await start_scheduler()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        print("bot started")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("bot deactivated")
