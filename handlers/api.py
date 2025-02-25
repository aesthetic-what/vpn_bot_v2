from fastapi import FastAPI, Request
from aiogram import Bot
from decouple import config
import asyncio

import uvicorn

app = FastAPI()
bot = Bot(token=config("TELEGRAM_TOKEN"))

@app.post("/yookassa_webhook/")
async def yookassa_webhook(request: Request):
    data = await request.json()
    if data["event"] == "payment.succeeded":
        payment_id = data["object"]["id"]
        chat_id = data["object"]["metadata"]["chat_id"]
        await bot.send_message(chat_id, "✅ Оплата получена!")
    return {"status": "ok"}


