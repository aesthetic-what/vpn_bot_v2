from apscheduler.schedulers.asyncio import AsyncIOScheduler
from yookassa import Payment
from logger import Logger
from redis.asyncio import Redis
from aiogram import Bot
import os

token = os.getenv("TELEGRAM_TOKEN")

scheduler = AsyncIOScheduler()
logger = Logger.getinstance()
bot = Bot(token=token)

redis = Redis(host="localhost", port=6379, db=0, decode_responses=True)

async def check_payments():
    """Функция для фоновой проверки оплаты,
    после успешной проверки, пользователь получает ключ для подключения к впн"""
    payments = await redis.hgetall(
        "payments"
    )  # Получаем платежи как {payment_id: chat_id}

    logger.info(f"Найдено {len(payments)} платежей для проверки")

    for chat_id, payment_id in payments.items():
        if not isinstance(payment_id, str):
            logger.info(f"payment_id: {payment_id}")
            logger.error(f"Ошибка: неверный payment_id = {payment_id}")
            continue

        payment = Payment.find_one(payment_id)

        if payment and payment.status == "succeeded":
            await bot.send_message(chat_id, "✅ Ваш платеж успешно подтвержден!\n"
                                            "Ваша подписка продлена")

            # функция для генерации и выдачи ключа
            logger.info(f"сумма покупки: {payment.amount.currency}")
            if payment.amount.currency == 1:
                ...

            # Логируем перед удалением
            logger.info(f"Удаляю payment_id: {payment_id} из Redis")
            await redis.hdel("payments", chat_id)  # Удаляем payment_id

            # Проверяем, остались ли платежи
            remaining_payments = await redis.hlen("payments")
            if remaining_payments == 0:
                job = scheduler.get_job("check_payments")
                if job:
                    scheduler.pause_job("check_payments")
                    logger.info("Все платежи обработаны, проверка остановлена")

    await redis.close()



async def start_scheduler():
    """Запуск планировщика"""
    scheduler.add_job(check_payments, "interval", seconds=5, id="check_payments")
    scheduler.start()


async def resume_scheduler():
    """Возобновить проверку платежей при добавлении нового платежа"""
    if not scheduler.get_job("check_payments"):
        scheduler.add_job(check_payments, "interval", seconds=5, id="check_payments")
    else:
        scheduler.resume_job("check_payments")
    logger.info("Проверка платежей возобновлена")

