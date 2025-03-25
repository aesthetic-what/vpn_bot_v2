from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.marzban_client import update_sub
from marzban import MarzbanAPI
from yookassa import Payment
from logger import Logger
from redis.asyncio import Redis
from aiogram import Bot
import time
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TELEGRAM_TOKEN")

scheduler = AsyncIOScheduler()
logger = Logger.getinstance()
bot = Bot(token=token)

redis = Redis(host="redis", port=6379, db=0, decode_responses=True)
# redis = Redis(host="localhost", port=6379, db=0, decode_responses=True)

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
                                            "Подписка успешно продлена")

            # функция для генерации и выдачи ключа
            logger.info(f"сумма покупки: {int(payment.amount.value)}")

            payment_amount = int(payment.amount.value)

            if payment_amount == 200:
                logger.info("subscribe 1 month")
                await update_sub(chat_id, 30, 0)
            elif payment_amount == 600:
                logger.info("subscribe 3 months")
                await update_sub(chat_id, 90, 0)
            elif payment_amount == 1200:
                logger.info("subscribe 6 months")
                await update_sub(chat_id, 186)

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
    # scheduler.add_job(check_payments, "interval", seconds=5, id="check_payments")
    scheduler.start()
    scheduler.add_job(check_status, "interval", hours=24, id="status_checker")
    logger.info(scheduler.get_jobs())


async def resume_scheduler():
    """Возобновить проверку платежей при добавлении нового платежа"""
    logger.info(scheduler.get_jobs())
    if not scheduler.get_job("check_payments"):
        scheduler.add_job(check_payments, "interval", seconds=5, id="check_payments")
    else:
        scheduler.resume_job("check_payments")
    logger.info("Проверка платежей возобновлена")


async def check_status():
    """Планировщик для проверки кол-ва дней подписки"""
    username = os.getenv("USERNAME_API")
    password = os.getenv("PASSWORD_API")
    api_url = os.getenv("API_URL")

    reminder_time = 3 * 86400

    api = MarzbanAPI(api_url)
    token = await api.get_token(username, password)

    users = await api.get_users(token.access_token)
    for user in users.users:
        while True:
            expire_time = user.expire
            chat_id = user.username
            print(chat_id)
            if expire_time == None:
                continue
            if expire_time and (expire_time - int(time.time())) <= reminder_time:
                message = f"Ваша подписка истекает через `{((expire_time - int(time.time())) // 86400)} дня(-ей)`. Рекомендую продлить подписку для стабильной работы впн"
                # Отправляем напоминание
                await bot.send_message(chat_id, text=message, parse_mode="Markdown")

