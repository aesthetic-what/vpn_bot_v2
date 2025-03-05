from handlers.client import *
from dotenv import load_dotenv
from handlers.db.sql_routers import *
from handlers.db.db_core import *
from py3xui import Inbound
from datetime import datetime
import asyncio
import uuid

load_dotenv(override=True)

async def main():
    await init_db()
    user_uuid = str(uuid.uuid4())

    # await create_user_vpn("1", 100)
    await update_client_key("sigmochka")
    
    
asyncio.run(main())
