from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.marzban_client import update_sub, get_days, get_users_
from handlers.db.sql_routers import set_paid, get_referrer
import handlers.keyboard as kb
from marzban import MarzbanAPI
from yookassa import Payment
from logger import Logger
from redis.asyncio import Redis
from aiogram import Bot
from datetime import datetime, timedelta
from dotenv import load_dotenv
import asyncio
import time
import os

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
            await get_referrer(chat_id)
            await set_paid(chat_id)

            # функция для генерации и выдачи ключа
            logger.info(f"сумма покупки: {int(payment.amount.value)}")

            payment_amount = int(payment.amount.value)

            if payment_amount == 2:
                logger.info("sub test")

            if payment_amount == 250:
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
            logger.info(f"🔍 Количество оставшихся платежей: {remaining_payments}")

            if remaining_payments == 0:
                job = scheduler.get_job("check_payments")
                if job:
                    scheduler.remove_job("check_payments")  # Удаляем задачу
                    logger.info("✅ Все платежи обработаны, проверка ОСТАНОВЛЕНА")
                else:
                    logger.warning("⚠️ Задача check_payments не найдена")

    await redis.close()


async def reconnect_redis():
    global redis
    for _ in range(5):  # 5 попыток переподключения
        try:
            redis = await redis.from_url("redis://localhost", decode_responses=True)
            logger.info("🔄 Успешное переподключение к Redis")
            return
        except Exception as e:
            logger.error(f"❌ Ошибка переподключения к Redis: {e}")
            await asyncio.sleep(2)  # Ждём 2 секунды перед новой попыткой
    logger.critical("🚨 Не удалось переподключиться к Redis после 5 попыток!")


async def cancel_payment(chat_id):
    """Отмена платежа через 2 минуты, если не оплачен"""
    try:
        if await redis.hexists("payments", chat_id):  # Проверяем, остался ли платеж в Redis
            logger.info(f"❌ Платёж {chat_id} не прошел за 2 минуты, удаляем...")
            await redis.hdel("payments", chat_id)  # Удаляем платеж
             # Проверяем, остались ли платежи
            remaining_payments = await redis.hlen("payments")
            logger.info(f"🔍 Количество оставшихся платежей: {remaining_payments}")

            if remaining_payments == 0:
                job = scheduler.get_job("check_payments")
                if job:
                    scheduler.remove_job("check_payments")  # Удаляем задачу
                    logger.info("✅ Все платежи обработаны, проверка ОСТАНОВЛЕНА")
                else:
                    logger.warning("⚠️ Задача check_payments не найдена")
            if scheduler.get_job(f"cancel_{chat_id}"):  # Проверяем перед удалением
                scheduler.remove_job(f"cancel_{chat_id}")
            else:
                logger.warning(f"⚠️ Задача cancel_{chat_id} уже отсутствует")
  # Удаляем задачу отмены из планировщика
    except redis.exceptions.ConnectionError as e:
        logger.error(f"Ошибка подключения к Redis: {e}")
        await reconnect_redis()
    except Exception as e:
        logger.error(f"Ошибка в cancel_payment: {e}")


async def start_payment_check(chat_id: str, payment_id: str | None = None):
    """Добавление платежа в Redis и запуск проверок"""
    await redis.hset("payments", chat_id, payment_id)

    # Запуск проверки каждые 10 секунд (если не запущена)
    if not scheduler.get_job("check_payments"):
        scheduler.add_job(check_payments, "interval", seconds=5, id="check_payments")

    # Запускаем таймер на 2 минуты для отмены платежа
    run_time = datetime.now() + timedelta(seconds=40)
    scheduler.add_job(cancel_payment, "date", run_date=run_time, id=f"cancel_{chat_id}", args=[chat_id],
                      replace_existing=True)


async def start_scheduler():
    """Запуск планировщика"""
    # scheduler.add_job(check_payments, "interval", seconds=5, id="check_payments")
    scheduler.start()
    scheduler.add_job(check_status, "interval", hours=24, id="status_checker")
    logger.info(scheduler.get_jobs())


async def resume_scheduler(chat_id: str, payment_id: str):
    """Возобновить проверку платежей при добавлении нового платежа"""
    logger.info(scheduler.get_jobs())
    if not scheduler.get_job("check_payments"):
        await start_payment_check(chat_id, payment_id)
    else:
        scheduler.resume_job("check_payments")
    logger.info("Проверка платежей возобновлена")


async def check_status():
    """Планировщик для проверки кол-ва дней подписки"""
    reminder_day = 1

    users = await get_users_()
    for user in users.users:
        expire_time = user.expire
        if not expire_time:
            continue
        chat_id = user.username

        days = await get_days(chat_id)
        print(f"user: {chat_id}, expire_time: {days}")

        if expire_time == None:
            continue
        if expire_time and days == reminder_day:
            message = f"У вас остался 1 день\nЗавтра доступ к VPN отключится, чтобы данный момент не доставил проблем, оплатите подписку заранее"
            # Отправляем напоминание
            await bot.send_message(chat_id, text=message, parse_mode="Markdown", reply_markup=kb.one_day_keyboard.as_markup())
        elif user.status == "expired":
            message = f"Срок бесплатного периода закончился\nДля продолжения использования оплатите подписку"
            # Отправляем напоминание
            await bot.send_message(chat_id, text=message, parse_mode="Markdown", reply_markup=kb.zero_day_keyboard.as_markup())
