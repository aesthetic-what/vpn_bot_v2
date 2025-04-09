from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery
from aiogram.types.web_app_info import WebAppInfo
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token)
keyboard = Router(name="keyboard")

status_keyboard = InlineKeyboardBuilder()
_go_back = InlineKeyboardButton(text='Назад', callback_data="go_back")
status_keyboard.add(_go_back)
status_keyboard.adjust(1)


menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="ℹ️ Статус"),KeyboardButton(text="⚡️ Подключиться")],
        [KeyboardButton(text="🔥 Купить"), KeyboardButton(text="❓ Помощь")],
    ],
    resize_keyboard=True,
)



buy_keyboard = InlineKeyboardBuilder()

_but_1 = InlineKeyboardButton(text="✅1 месяц", callback_data="1")
_but_2 = InlineKeyboardButton(text="💥3 месяца", callback_data="3")
_but_3 = InlineKeyboardButton(text="🚀6 месяцев", callback_data="6")
_but_4 = InlineKeyboardButton(text="Назад", callback_data="go_back")
list_buttons = [_but_1, _but_2, _but_3, _but_4]

for button in list_buttons:
    buy_keyboard.add(button)
buy_keyboard.adjust(1)

var_payment_keyboard = InlineKeyboardBuilder()

_var_1 = InlineKeyboardButton(text="✨stars", callback_data="stars")
_var_2 = InlineKeyboardButton(text="yookassa", callback_data="yookassa")
_var_3 = InlineKeyboardButton(text="back", callback_data="go_back_payment")

list_var = [_var_1, _var_2, _var_3]

for button in list_var:
    var_payment_keyboard.add(button)
var_payment_keyboard.adjust(2)

connect_keyboard = InlineKeyboardBuilder()

_con_1 = InlineKeyboardButton(text="🍎скачать", url="https://apps.apple.com/ru/app/v2raytun/id6476628951")
# _con_2 = InlineKeyboardButton(text="подключить", url=f"hiddify://import/{sub_url}")
_con_3 = InlineKeyboardButton(text="📱скачать", url="https://play.google.com/store/apps/details?id=com.v2raytun.android")
# _con_4 = InlineKeyboardButton(text="подключить", url=f"hiddify://import/{sub_url}")
_con_5 = InlineKeyboardButton(text="🖥️скачать", url="https://github.com/hiddify/hiddify-next/releases/latest/download/Hiddify-Windows-Setup-x64.exe")
# _con_6 = InlineKeyboardButton(text="подключить", url=f"hiddify://import/{sub_url}")
_con_7 = InlineKeyboardButton(text="назад", callback_data="go_back")

# list_connect = [_con_1, _con_2, _con_3, _con_4, _con_5, _con_6, _con_7]
list_connect = [_con_1, _con_3, _con_5, _con_7]

for button in list_connect:
    connect_keyboard.add(button)
connect_keyboard.adjust(3)


help_keyboard = InlineKeyboardBuilder()

_help_1 = InlineKeyboardButton(text="🍎подключить IOS", url="https://telegra.ph/Podklyuchenie-Hiddify-IOS-03-13")
_help_2 = InlineKeyboardButton(text="📱подключить Android", url="https://telegra.ph/Podklyuchenie-Hiddify-Android-03-13")
_help_3 = InlineKeyboardButton(text="🖥️подключить Windows", url="https://telegra.ph/Podklyuchenie-VPN-na-Windows-03-13")
_help_4 = InlineKeyboardButton(text="поддержка", url="https://t.me/aesthetic_what")
_help_5 = InlineKeyboardButton(text="назад", callback_data="go_back")

list_help = [_help_1, _help_2, _help_3, _help_4, _help_5]

for button in list_help:
    help_keyboard.add(button)
help_keyboard.adjust(1)


one_day_keyboard = InlineKeyboardBuilder()

_one_day = InlineKeyboardButton(text='Оплатить', callback_data="pay_sub_one")
one_day_keyboard.add(_one_day)
one_day_keyboard.adjust(1)
one_day_keyboard

zero_day_keyboard = InlineKeyboardBuilder()

_zero_day = InlineKeyboardButton(text='Продлить сейчас', callback_data="pay_sub_one")
zero_day_keyboard.add(_zero_day)
zero_day_keyboard.adjust(1)
zero_day_keyboard


async def stars_payment(price: int, chat_id: str):
    buy_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оплатить", pay=True)],
            [InlineKeyboardButton(text='Назад', callback_data='go_back')]]
    )
    prices = [LabeledPrice(label="XTR", amount=price)]
    return await bot.send_invoice(
        chat_id=chat_id,
        title="подписка Kitty GPT",
        description=f"Купить подписку Kitty GPT\nЦена: {price}",
        prices=prices,
        provider_token="STARS",
        payload="channel_support",
        currency="XTR",
        reply_markup=buy_keyboard,
    )

def get_var_payment_keyboard(price: int) -> InlineKeyboardMarkup:
    """Генерирует клавиатуру с выбором способа оплаты и передает цену через callback_data."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оплатить Звездами", callback_data=f"stars_payment:{price}")],
            [InlineKeyboardButton(text="Оплатить через ЮKassa", callback_data=f"yookassa_pay:{price}")],
            [InlineKeyboardButton(text='Назад', callback_data='go_back')]
        ]
    )
    return keyboard

def payment_yookassa_keyboard(payment_url: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Оплатить', url=payment_url)],
            [InlineKeyboardButton(text='Назад', callback_data="go_to_choose_payment")]
            ]
    )
    return keyboard

def sub_link_keyboard(sub_link: str) -> InlineKeyboardMarkup:
    """Тестовая клавиатура для проверки веб апп"""
    keyboard = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text='перейти в веб апп', web_app=WebAppInfo(url=sub_link))
    keyboard.add(button)
    keyboard.adjust(1)
    return keyboard.as_markup()

# # @router.pre_checkout_query()
# @router.message(Command('buy'))
# async def send_invoice_handler(message: Message):
#     try:
#         price = int(message.text.split()[1])
#         prices = [LabeledPrice(label="XTR", amount=price)]
#         await bot.send_invoice(
#             chat_id=message.chat.id,
#             title="подписка Kitty GPT",
#             description=f"Купить подписку Kitty GPT\nЦена: {price}",
#             prices=prices,
#             provider_token="STARS",
#             payload="channel_support",
#             currency="XTR",
#             reply_markup=kb.buy_keyboard,
#         )
#     except IndexError:
#         await message.answer("Введите число после команды")
