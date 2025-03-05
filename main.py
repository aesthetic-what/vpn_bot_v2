from aiogram import Bot, Dispatcher
# from decouple import config
import asyncio
import uvicorn

from handlers.handlers import router
from handlers.db.db_core import init_db
from logger import Logger
from dotenv import load_dotenv
import os

load_dotenv()

logger = Logger.getinstance()

async def main():
    await init_db()
    bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

# async def api():
#     uvicorn.run(app="handlers.api:app", host="127.0.0.1", port=8000, reload=True)

# async def main():
#     await asyncio.gather(bot(), api())

if __name__ == '__main__':
    try:
        print('bot started')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('bot deactivated')