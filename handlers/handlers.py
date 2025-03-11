from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F, Bot
from redis.asyncio import Redis

from handlers.marzban_client import *
from handlers.scheduler import *
from handlers.payments import *
from logger import Logger

import handlers.keyboard as kb
import os


logger = Logger.getinstance()
redis = Redis(host="localhost", port=6379, db=0, decode_responses=True)
router = Router(name="handlers")
bot = Bot(os.getenv("TELEGRAM_TOKEN"))


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
    await resume_scheduler()
    await call.bot.answer_callback_query(call.id)


@router.callback_query(F.data == "3")
async def tarif_1(call: CallbackQuery):
    price = 600
    payment_url, payment_id = create_payment(price, call.message.chat.id, 3)
    chat_id = call.message.chat.id

    await call.message.answer(
        "Тариф: 3 месяц\nЦена: 600руб.\nВыберите удобный для вас способ оплаты:",
        reply_markup=kb.get_var_payment_keyboard(price, payment_url),
    )

    logger.info(f"chat_id: {chat_id}, payment_id: {payment_id}")
    await save_payment(chat_id, payment_id)
    await resume_scheduler()
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

    logger.info(f"chat_id: {chat_id}, payment_id: {payment_id}")
    await save_payment(chat_id, payment_id)
    await resume_scheduler()
    await call.bot.answer_callback_query(call.id)


@router.message(F.text == "⚡️ Подключисться!")
async def connect(message: Message):

    sub_link = await trial_sub(str(message.chat.id), 10, 30)
    await message.answer(
        "вот способы подключения к впн:\n"
        "описание\n"
        "сслыка для ручного подключения:\n"
        f"`{sub_link}`",
        reply_markup=kb.connect_keyboard.as_markup(),
        parse_mode="Markdown"
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
