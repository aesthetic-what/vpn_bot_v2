from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F, Bot
from redis.asyncio import Redis

from handlers.marzban_client import *
from handlers.db.sql_routers import *
from handlers.scheduler import *
from handlers.payments import *
from dotenv import load_dotenv
from logger import Logger

import handlers.keyboard as kb
import os

load_dotenv()
logger = Logger.getinstance()
redis = Redis(host="redis", port=6379, db=0, decode_responses=True)
# redis = Redis(host="localhost", port=6379, db=0, decode_responses=True)
router = Router(name="handlers")
bot = Bot(os.getenv("TELEGRAM_TOKEN"))




def format_bytes(bytes_value: int) -> str:
    """Форматирует байты в человекочитаемый формат"""
    if not bytes_value:
        return "0 B"
    
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    while bytes_value >= 1024 and i < len(suffixes)-1:
        bytes_value /= 1024.
        i += 1
    return f"{bytes_value:.2f} {suffixes[i]}"

def format_date(timestamp: int) -> str:
    """Форматирует timestamp в читаемую дату"""
    if not timestamp:
        return "Не ограничено"
    return datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y %H:%M")


@router.message(CommandStart())
async def start(message: Message):
    args = message.text.split()
    referrer_id = None
    username = message.from_user.first_name
    chat_id = str(message.chat.id)

    user_exists = await check_user(chat_id)
    # logger.info(user_exists)

    if len(args) > 1 and args[1].startswith("ref_"):
        referrer_id = str(args[1][4:])

    logger.info(referrer_id)

    if not user_exists:
        await create_user(username, chat_id, referrer_id)

    await message.answer(
        "👋 Здравствуйте. Это Telegram-бот для подключения к VPN.\nВам доступен бесплатный период - 10 дней.\nДля начала работы нажмите ⚡️Подключиться ↓",
        reply_markup=kb.menu_keyboard
    )


@router.message(F.text == "ℹ️ Статус")
async def info(message: Message):
    user = await get_user_info(str(message.chat.id))


    if user.sub_link:
        info = await user_sub_info(str(message.chat.id))
        status_emoji = "🟢" if info.status == 'active' else "🔴"

        expire_date = format_date(info.expire)
        days = await get_days(str(message.chat.id))

        if info.status == "active":
            status = 'Активна'
        else:
            status = 'Не активна'

        await message.answer(f"Статус подписки: {status_emoji} {status}\n"
                            f"├ Осталось дней: {days}\n"
                            f"└ Активна до: {expire_date}\n\n"
                            f"Ваша партнерская ссылка:\n"
                            f"`https://t.me/KittyVPN_bot?start=ref_{user.user_id}`\n"
                            f"├Нажмите на нее, чтобы скопировать и отправьте друзьям\n"
                            f"└Всего: {user.invated_users} - Оплатили: {user.paid_users}", 
                            reply_markup=kb.status_keyboard.as_markup(),
                            parse_mode="Markdown")
        await message.bot.delete_message(message.chat.id, message.message_id)
    else:
        await message.answer("Вы еще не активировали свой ключ, для этого нажмите ниже\n⚡️ Подключиться\n\n"
                             "🔴Пригласи друга и получи 25 дней БЕСПЛАТНО, если он оплатит подписку!"
                            f"Ваша партнерская ссылка:\n"
                            f"`https://t.me/KittyVPN_bot?start=ref_{user.user_id}`\n"
                            f"├Нажмите на нее, чтобы скопировать и отправьте друзьям\n"
                            f"└Всего: {user.invated_users} - Оплатили: {user.paid_users}",
                            parse_mode="Markdown")
        await message.bot.delete_message(message.chat.id, message.message_id)

@router.callback_query(F.data == 'pay_sub_one')
async def buy(call: CallbackQuery):
    await call.message.answer("Выберите тариф:", reply_markup=kb.buy_keyboard.as_markup())
    await call.bot.answer_callback_query(call.id)
    # await call.message.bot.delete_message(call.message.chat.id, call.message.message_id)

@router.callback_query(F.data == 'go_to_choose_payment')
async def choose_payment(call: CallbackQuery):
    await call.message.answer("Выберите тариф:", reply_markup=kb.buy_keyboard.as_markup())
    await call.bot.answer_callback_query(call.id)

@router.callback_query(lambda call: call.data.startswith("yookassa"))
async def yookassa_pay(call: CallbackQuery):
    chat_id = str(call.message.chat.id)

    user = await get_user_info(chat_id)
    sub_link = user.sub_link
    if sub_link:
        price = call.data.split(":")[-1]
        payment_url, payment_id = create_payment(price, chat_id)
        await call.message.answer(text="Оплатить можно через СБП, МИР", 
                                reply_markup=kb.payment_yookassa_keyboard(payment_url))
        logger.info(f"chat_id: {chat_id}, payment_id: {payment_id}")
        await save_payment(chat_id, payment_id)
        await resume_scheduler(chat_id, payment_id)
    else:
        await call.answer("Для начала нажмите ⚡️ Подключиться для получения ключа", show_alert=True)
    await call.bot.answer_callback_query(call.id)


@router.message(F.text == "🔥 Купить")
async def buy(message: Message):
    await message.answer("Выберите тариф:", reply_markup=kb.buy_keyboard.as_markup())
    await message.bot.delete_message(message.chat.id, message.message_id)


@router.callback_query(F.data == "1")
async def tarif_1(call: CallbackQuery):
    price = 250
    await call.message.answer(
        "Тариф: 1 месяц\nЦена: 250руб.\nВыберите удобный для вас способ оплаты:",
        reply_markup=kb.get_var_payment_keyboard(price),
    )
    await call.bot.answer_callback_query(call.id)


@router.callback_query(F.data == "3")
async def tarif_1(call: CallbackQuery):
    price = 600
    await call.message.answer(
        "Тариф: 3 месяц\nЦена: 600руб.\nВыберите удобный для вас способ оплаты:",
        reply_markup=kb.get_var_payment_keyboard(price),
    )
    await call.bot.answer_callback_query(call.id)


@router.callback_query(F.data == "6")
async def tarif_1(call: CallbackQuery):
    price = 1200
    await call.message.answer(
        "Тариф: 6 месяц\nЦена: 1200руб.\nВыберите удобный для вас способ оплаты:",
        reply_markup=kb.get_var_payment_keyboard(price),
    )
    await call.bot.answer_callback_query(call.id)

@router.message(F.text == "⚡️ Подключиться")
async def connect(message: Message):
    logger.info("connect button")
    chat_id = str(message.chat.id)

    # Проверяем, есть ли пользователь в базе
    user_exists = await check_user(chat_id)
    logger.info(user_exists)

    if user_exists:
        logger.info("user exist")
        # Если пользователя нет, создаём пробную подписку и записываем в БД
        user_link, expire_time = await trial_sub(chat_id, 10, 30)
        await update_user(chat_id, user_link, expire_time)

    await message.answer(
        "Доступ к VPN в 2 шага:\n\n"
        "1️⃣ `Скачать` - для скачивания приложения\n"
        f"2️⃣ `Подключить` - для добавления подписки\n\nНастроить VPN вручную:\n"
        "- [Инструкция для Android](https://telegra.ph/Podklyuchenie-Hiddify-Android-03-13) 🤖\n"
        "- [Инструкция для Iphone](https://telegra.ph/Podklyuchenie-Hiddify-IOS-03-13) 🍎\n"
        "- [Инструкция для Windows](https://telegra.ph/Podklyuchenie-VPN-na-Windows-03-13) 🖥️\n\n"
        "Ссылка для ручного подключения\n"
        "Тапните чтобы скопировать в буфер обмена ↓\n\n"
        f"`{user_link}`\n",
        reply_markup=kb.connect_keyboard.as_markup(),
        parse_mode="Markdown",
        disable_web_page_preview=True
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
    # scheduler.remove_job("check_payments")
    # price = int(call.data.split(":")[1])
    # await kb.stars_payment(price, call.message.chat.id)
    # await call.bot.answer_callback_query(call.id)
    await call.answer("Данный способ еще в разработке")


@router.callback_query(F.data == "go_back")
async def back(call: CallbackQuery):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.bot.answer_callback_query(call.id)

@router.callback_query(F.data == "go_back_payment")
async def back(call: CallbackQuery):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.bot.answer_callback_query(call.id)
    scheduler.remove_job("check_payments")
