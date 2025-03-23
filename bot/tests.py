# from handlers.scheduler import check_status
from dotenv import load_dotenv
from handlers.db.sql_routers import *
from handlers.db.db_core import *
import asyncio

load_dotenv(override=True)

async def main():
    print(os.getenv("TELEGRAM_TOKEN"))
    await init_db()
    
asyncio.run(main())
