# from handlers.scheduler import check_status
from dotenv import load_dotenv
from handlers.db.sql_routers import *
from handlers.db.db_core import *
from handlers.scheduler import check_status
from handlers.payments import create_payment
from handlers.marzban_client import *
import asyncio

load_dotenv(override=True)

async def main():
    # await get_users_()
    # await check_status()
    payment_url, payment_id = create_payment(200, "123144352", 1)
    print(payment_id, payment_url)
    
asyncio.run(main())

