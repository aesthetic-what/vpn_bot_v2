from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from handlers.payments import *
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
import handlers.keyboard as kb
from redis.asyncio import Redis
from handlers.xui import *
import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

redis = Redis(host="localhost", port=6379, db=0, decode_responses=True)

# jobStores = {
#     "default": RedisJobStore(
#         jobs_key="dispatched_trips_jobs",
#         run_times_key="dispatched_trips_running",
#         host="localhost",
#         port=6379,
#     )
# }

router = Router(name="handlers")

scheduler = AsyncIOScheduler()

bot = Bot(config("TELEGRAM_TOKEN"))


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Здравствуйте. Это Telegram-бот для подключения к VPN.\nВам доступен бесплатный период - 10 дней.\nДля начала работы нажмите ⚡️Подключиться ↓",
        reply_markup=kb.menu_keyboard,
    )


@router.message(F.text == "ℹ️ Статус")
async def info(message: Message):
    await message.answer("Статус аккаунта")
    await message.bot.delete_message(message.chat.id, message.message_id)


@router.message(F.text == "🔥 Купить")
async def buy(message: Message):
    await message.answer("Выберите тариф:", reply_markup=kb.buy_keyboard.as_markup())
    await message.bot.delete_message(message.chat.id, message.message_id)


@router.callback_query(F.data == "1")
async def tarif_1(call: CallbackQuery):
    price = 200
    payment_url, payment_id = create_payment(price, call.message.chat.id, 3)
    await call.message.answer(
        "Тариф: 1 месяц\nЦена: 200руб.\nВыберите удобный для вас способ оплаты:",
        reply_markup=kb.get_var_payment_keyboard(price, payment_url),
    )

    chat_id = call.message.chat.id
    logger.info(f"chat_id: {chat_id}, payment_id: {payment_id}")
    await save_payment(chat_id, payment_id)
    await start_scheduler()
    await call.bot.answer_callback_query(call.id)


@router.callback_query(F.data == "3")
async def tarif_1(call: CallbackQuery):
    price = 600
    payment_url, payment_id = create_payment(price, call.message.chat.id, 3)
    chat_id = call.message.chat.id
    # await save_payment(chat_id, payment_id)

    await call.message.answer(
        "Тариф: 3 месяц\nЦена: 600руб.\nВыберите удобный для вас способ оплаты:",
        reply_markup=kb.get_var_payment_keyboard(price, payment_url),
    )
    await call.bot.answer_callback_query(call.id)


@router.callback_query(F.data == "6")
async def tarif_1(call: CallbackQuery):
    price = 1200
    payment_url, payment_id = create_payment(price, call.message.chat.id, 3)
    chat_id = call.message.chat.id

    await call.message.answer(
        "Тариф: 6 месяц\nЦена: 1200руб.\nВыберите удобный для вас способ оплаты:",
        reply_markup=kb.get_var_payment_keyboard(price, payment_url),
    )
    await call.bot.answer_callback_query(call.id)


@router.message(F.text == "⚡️ Подключисться!")
async def connect(message: Message):
    expiry_timestamp = int(time.time()) + (7 * 86400)

    await create_inbound(message.from_user.first_name, message.chat.id, expiry_timestamp)  

    await message.answer(
        "вот способы подключения к впн:", reply_markup=kb.connect_keyboard.as_markup()
    )
    await message.bot.delete_message(message.chat.id, message.message_id)


@router.message(F.text == "❓ Помощь")
async def help(message: Message):
    await message.answer(
        "Если у вас возникли проблемы с подключением. ниже представлены инструкции:",
        reply_markup=kb.help_keyboard.as_markup(),
    )
    await message.bot.delete_message(message.chat.id, message.message_id)


@router.callback_query(F.data.startswith("stars_payment"))
async def stars(call: CallbackQuery):
    price = int(call.data.split(":")[1])
    await kb.stars_payment(price, call.message.chat.id)
    await call.bot.answer_callback_query(call.id)


@router.callback_query(F.data == "go_back")
async def back(call: CallbackQuery):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.bot.answer_callback_query(call.id)

async def check_payments():
    payments = await redis.hgetall("payments")  # Получаем платежи как {payment_id: chat_id}

    logger.info(f"Найдено {len(payments)} платежей для проверки")

    for chat_id, payment_id in payments.items():
        if not isinstance(payment_id, str):
            logger.info(f"payment_id: {payment_id}")
            logger.error(f"Ошибка: неверный payment_id = {payment_id}")
            continue

        payment = Payment.find_one(payment_id)

        if payment and payment.status == "succeeded":
            await bot.send_message(chat_id, "✅ Ваш платеж успешно подтвержден!")

            # Логируем перед удалением
            logger.info(f"Удаляю payment_id: {payment_id} из Redis")

            await redis.hdel("payments", chat_id)  # Удаляем payment_id

            # Удаляем задачу, если есть
            job_id = f"payment_{payment_id}"
            if scheduler.get_job(job_id):
                scheduler.remove_job(job_id)

    await redis.close()




async def start_scheduler():
    scheduler.add_job(check_payments, "interval", seconds=10, jobstore="default")
    scheduler.start()
