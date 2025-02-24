from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

import handlers.keyboard as kb

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('👋 Здравствуйте. Это Telegram-бот для подключения к VPN.\nВам доступен бесплатный период - 10 дней.\nДля начала работы нажмите ⚡️Подключиться ↓',
                         reply_markup=kb.menu_keyboard)

@router.message(F.text == 'ℹ️ Статус')
async def info(message: Message):
    await message.answer('Статус аккаунта')

@router.message(F.text == '🔥 Купить')
async def buy(message: Message):
    await message.answer('Выберите тариф:',
                         reply_markup=kb.buy_keyboard.as_markup())

@router.message(F.text == '⚡️ Подключисться!')
async def connect(message: Message):
    await message.answer('вот способы подключения к впн:',
                         reply_markup=kb.connect_keyboard.as_markup())

@router.message(F.text == '❓ Помощь')
async def help(message: Message):
    await message.answer('Если у вас возникли проблемы с подключением. ниже представлены инструкции:',
                         reply_markup=kb.help_keyboard.as_markup())