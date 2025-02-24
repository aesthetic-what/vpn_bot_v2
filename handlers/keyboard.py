from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='ℹ️ Статус'), KeyboardButton(text='⚡️ Подключисться!')],
    [KeyboardButton(text='🔥 Купить'), KeyboardButton(text='❓ Помощь')]], resize_keyboard=True)

buy_keyboard = InlineKeyboardBuilder()

_but_1 = InlineKeyboardButton(text='1 месяц', callback_data='1')
_but_2 = InlineKeyboardButton(text='3 месяца', callback_data='3')
_but_3 = InlineKeyboardButton(text='6 месяцев', callback_data='6')
_but_4 = InlineKeyboardButton(text='Назад', callback_data='back')
list_buttons = [_but_1, _but_2, _but_3, _but_4]

for button in list_buttons:
    buy_keyboard.add(button)
buy_keyboard.adjust(1)


connect_keyboard = InlineKeyboardBuilder()

_con_1 = InlineKeyboardButton(text='скачать', callback_data='andr')
_con_2 = InlineKeyboardButton(text='подключить', callback_data='andr')
_con_3 = InlineKeyboardButton(text='скачать', callback_data='andr')
_con_4 = InlineKeyboardButton(text='подключить', callback_data='andr')
_con_5 = InlineKeyboardButton(text='скачать', callback_data='andr')
_con_6 = InlineKeyboardButton(text='подключить', callback_data='andr')
_con_7 = InlineKeyboardButton(text='назад', callback_data='andr')

list_connect = [_con_1, _con_2, _con_3, _con_4, _con_5, _con_6, _con_7]

for button in list_connect:
    connect_keyboard.add(button)
connect_keyboard.adjust(2)


help_keyboard = InlineKeyboardBuilder()

_help_1 = InlineKeyboardButton(text='подключить IOS', callback_data='andr')
_help_2 = InlineKeyboardButton(text='подключить Android', callback_data='andr')
_help_3 = InlineKeyboardButton(text='подключить Windows', callback_data='andr')
_help_4 = InlineKeyboardButton(text='поддержка', callback_data='andr')
_help_5 = InlineKeyboardButton(text='назад', callback_data='andr')

list_help = [_help_1, _help_2, _help_3, _help_4, _help_5]

for button in list_help:
    help_keyboard.add(button)
help_keyboard.adjust(1)



