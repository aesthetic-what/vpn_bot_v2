import uuid
import os

from yookassa import Configuration, Payment
from redis.asyncio import Redis
from logger import Logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

load_dotenv()

logger = Logger.getinstance()
scheduler = AsyncIOScheduler()

acc_id = os.getenv("ACCOUNT_ID")
secret_key = os.getenv("SECRET_KEY")

redis = Redis(host="redis", port=6379, db=0, decode_responses=True)
# redis = Redis(host="localhost", port=6379, db=0, decode_responses=True)


async def save_payment(chat_id: str, payment_id: str | int):
    # redis = r.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)
    user = await redis.hget("payments", chat_id)
    if not user:
        await redis.hset("payments", chat_id, payment_id)
    else:
        await redis.hdel("payments", chat_id)
        await redis.set(chat_id, payment_id)
        await redis.close()


Configuration.account_id = acc_id
Configuration.secret_key = secret_key
# Configuration.account_id = "1041305"
# Configuration.secret_key = "test_PNTvM-9eEgTUUfjT6PnevgVi3kkTQKWJ3zcEYs2FHm4"


def create_payment(amount, chat_id, count):
    payment_id = str(uuid.uuid4())
    payment = Payment.create(
        {
            "amount": {
                "value": amount,
                "currency": "RUB",
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/KittyVPN_bot",
            },
            "capture": True,
            "description": "Оплата подписки",
            "metadata": {
                "chat_id": chat_id,
                "order_id": payment_id,
            },
            "description": f"Подписка на {count} месяц(a/ев)",
        },
        payment_id,
    )

    return payment.confirmation.confirmation_url, payment.id
