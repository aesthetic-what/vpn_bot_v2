import uuid
import os

from yookassa import Configuration, Payment, Receipt
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


def create_receipt(amount, payment_id: str, chat_id: str):
    receipt = Receipt.create({
                "customer": {
                    "email": f"{chat_id}@gmail.com",
                },
                "type": "payment",
                "payment_id": payment_id,
                "send": True,
                "items": [
                    {
                        "description": f"Подписка KittyV##",
                        "quantity": 1.000,
                        "amount": {
                            "value": f"{amount}.00",
                            "currency": "RUB"
                        },
                        "vat_code": 1,
                        "payment_mode": "full_payment",
                        "payment_subject": "service"
                    }
                ],
                "tax_system_code": 1,
                "settlements": [
                    {
                        "type": "cashless",
                        "amount": {
                            "value": f"{amount}.00",
                            "currency": "RUB"
                        }
                    }
                ],
            },
            payment_id)
    return receipt

def create_payment(amount: str, chat_id: str):
    payment_id = str(uuid.uuid4())

    # receipt = create_receipt(count, amount, payment_id, chat_id)

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
            "receipt": {
                "customer": {
                    "email": f"{chat_id}@gmail.com",
                },
                "type": "payment",
                "payment_id": payment_id,
                "send": True,
                "items": [
                    {
                        "description": f"Подписка услуги телеграмм бота",
                        "quantity": 1.000,
                        "amount": {
                            "value": f"{amount}.00",
                            "currency": "RUB"
                        },
                        "vat_code": 1,
                        "payment_mode": "full_payment",
                        "payment_subject": "service"
                    }
                ],
                "tax_system_code": 1,
                "settlements": [
                    {
                        "type": "cashless",
                        "amount": {
                            "value": f"{amount}.00",
                            "currency": "RUB"
                        }
                    }
                ],
            },
            "metadata": {
                "chat_id": chat_id,
                "order_id": payment_id,
            },
            "description": f"Подписка KittyV##",
        },payment_id)

    
    return payment.confirmation.confirmation_url, payment.id