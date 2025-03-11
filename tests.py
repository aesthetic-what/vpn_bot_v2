from handlers.marzban_client import *
from dotenv import load_dotenv
from handlers.db.sql_routers import *
from handlers.db.db_core import *
from datetime import datetime
import asyncio
import uuid

load_dotenv(override=True)

async def main():
    # await token()
    await test_marzban()
    
asyncio.run(main())
