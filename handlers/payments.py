import uuid

from yookassa import Configuration, Payment
from decouple import config

acc_id = config("ACCOUNT_ID")
secret_key = config("SECRET_KEY")

Configuration.account_id = '989951'
Configuration.secret_key = 'live_TVbe6YpKTdOqawLKLjRq0icralev2G5M9BRFvx03JyU'


def create_payment(amount, chat_id, count):
    payment_id = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": amount,
            "currency": "RUB",
        },
        # "payment_method_data": {
        #     "type": "sbp"
        # },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/KittyVPN_bot"
        },
        "capture": True,
        "description": "Оплата подписки",
        "metadata": {
        "chat_id": chat_id,
        "order_id": payment_id,
        },
        "description": f"Подписка на {count} месяц(a/ев)"
    }, payment_id)
    
    return payment.confirmation.confirmation_url, payment.id


def check(payment_id):
    payment = Payment.find_one(payment_id)

    if payment.status == 'succeeded':
        return payment.metadata, int(payment.income_amount.value)
    else:
        return False