import time
from marzban import (MarzbanAPI, 
                     UserCreate, 
                     UserModify, 
                     ProxySettings)

users = []

api_url = "https://aestheticperforator.ru"


import os

FILE_PATH = "users.txt"  # Файл для хранения tg_id

def load_users():
    """Загружает все ID пользователей из файла в список."""
    if not os.path.exists(FILE_PATH):
        return set()  # Если файла нет, возвращаем пустой set
    
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        return set(line.strip() for line in file.readlines())  # Убираем лишние пробелы и переносы строк

def save_user(tg_id):
    """Добавляет пользователя в файл, если его там нет."""
    users = load_users()  # Загружаем текущих пользователей
    if tg_id not in users:
        with open(FILE_PATH, "a", encoding="utf-8") as file:
            file.write(f"{tg_id}\n")  # Записываем нового пользователя



async def trial_sub(tg_id: str, days_sub: int, data_limit: int):
    api = MarzbanAPI(api_url)
    token = await api.get_token("admin", "jXCWh9Q7ImaZ")
    token = token.access_token

    __expiry_timestamp = int(time.time()) + (days_sub * 86400)
    __expiry_timestamp * 1000

    __data = data_limit * 2**30

    if not tg_id in load_users():
        new_user = UserCreate(
            username=tg_id,
            proxies={"vless": ProxySettings(flow="xtls-rprx-vision")},
            inbounds={"vless": ["VLESS TCP REALITY"]},
            data_limit=__data,
            expire=__expiry_timestamp,
        )
        add_user = await api.add_user(new_user, token)
        save_user(tg_id)
        return api_url + add_user.subscription_url
    else:
        user = await api.get_user(tg_id, token)
        return api_url + user.subscription_url


async def update_sub(tg_id: str, days_sub: int, data_limit: int):
    api = MarzbanAPI(api_url)
    token = await api.get_token("admin", "jXCWh9Q7ImaZ")
    token = token.access_token

    __expiry_timestamp = int(time.time()) + (days_sub * 86400)
    __expiry_timestamp * 1000

    __data = data_limit * 2**30

    if tg_id in users:
        update_user = UserModify(expire=__expiry_timestamp, data_limit=__data)
        await api.modify_user(tg_id, update_user, token)
