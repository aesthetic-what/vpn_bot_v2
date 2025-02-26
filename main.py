from aiogram import Bot, Dispatcher
from decouple import config
import asyncio
import uvicorn

from handlers.handlers import router
from handlers.db.db_core import Base, engine
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='api.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    bot = Bot(token=config('TELEGRAM_TOKEN'))
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
        asyncio.run(init_db())
    except KeyboardInterrupt:
        print('bot deactivated')