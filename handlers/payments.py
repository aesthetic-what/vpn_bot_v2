import uuid
import asyncio
import json
import logging

from yookassa import Configuration, Payment
from decouple import config
from redis.asyncio import Redis

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="api.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

acc_id = config("ACCOUNT_ID")
secret_key = config("SECRET_KEY")

redis = Redis(host="localhost", port=6379, db=0, decode_responses=True)


async def save_payment(chat_id: str, payment_id: str | int):
    # redis = r.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)
    user = await redis.hget("payments", chat_id)
    if not user:
        await redis.hset("payments", chat_id, payment_id)
    else:
        await redis.hdel("payments", chat_id)
        await redis.set(chat_id, payment_id)
        await redis.close()


# Configuration.account_id = '989951'
# Configuration.secret_key = 'live_TVbe6YpKTdOqawLKLjRq0icralev2G5M9BRFvx03JyU'
Configuration.account_id = "1041305"
Configuration.secret_key = "test_PNTvM-9eEgTUUfjT6PnevgVi3kkTQKWJ3zcEYs2FHm4"


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
