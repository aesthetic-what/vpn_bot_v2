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

    # await create_user('sigma_bro', "123123123", user_uuid, datetime.now())
    await get_connection_string(Inbound, user_uuid, "15qu6big")
    
asyncio.run(main())
