from aiogram import Bot, Dispatcher
from decouple import config
import asyncio

from handlers.handlers import router
from handlers.db.db_core import Base, engine

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    bot = Bot(token=config('TELEGRAM_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        print('bot started')
        asyncio.run(main())
        asyncio.run(init_db())
    except KeyboardInterrupt:
        print('bot deactivated')