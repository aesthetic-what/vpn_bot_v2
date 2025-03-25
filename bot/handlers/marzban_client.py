import time
from marzban import (MarzbanAPI, 
                     UserCreate, 
                     UserModify, 
                     ProxySettings)
import os
from logger import Logger
from handlers.db.sql_routers import check_user, get_user_info

logger = Logger.getinstance()


api_url = os.getenv("API_URL")
FILE_PATH = "users.txt"  # Файл для хранения tg_id

async def get_users():
    api = MarzbanAPI(api_url)
    username = os.getenv("USERNAME_API")
    password = os.getenv("PASSWORD_API")

    logger.info(f"admin data: {username, password}")

    token = await api.get_token(username, password)
    token = token.access_token

    return await api.get_users(token)   


async def trial_sub(tg_id: str, days_sub: int, data_limit: int):
    api = MarzbanAPI(api_url)
    username = os.getenv("USERNAME_API")
    password = os.getenv("PASSWORD_API")

    logger.info(f"admin data: {username, password}")

    token = await api.get_token(username, password)
    token = token.access_token

    # checking = await check_user(tg_id)
    # print(checking)
    
    __expiry_timestamp = int(time.time()) + (days_sub * 86400)
    # __expiry_timestamp * 1000

    __data = data_limit * 2**30

    try:
        user = await api.get_user(tg_id, token)
        if user:
            return api_url + user.subscription_url
    except Exception as e:
        logger.warning(f"User {tg_id} not found, creating new one. Error: {e}")

    new_user = UserCreate(
        username=tg_id,
        proxies={"vless": ProxySettings(flow="xtls-rprx-vision")},
        inbounds={"vless": ["VLESS TCP REALITY"]},
        data_limit=__data,
        expire=__expiry_timestamp,
    )

    logger.info(f"{new_user.expire}, type: {type(new_user.expire)}")

    add_user = await api.add_user(new_user, token)
    return api_url + add_user.subscription_url, __expiry_timestamp
    

async def activate_sub(tg_id: str):
    api = MarzbanAPI(api_url)
    username = os.getenv("USERNAME_API")
    password = os.getenv("PASSWORD_API")

    logger.info(f"admin data: {username, password}")

    token = await api.get_token(username, password)
    token = token.access_token

    activate_user = UserModify(status="active")
    await api.modify_user(tg_id, activate_user, token)


async def update_sub(tg_id: str, days_sub: int, data_limit: int | None = None):
    api = MarzbanAPI(api_url)
    username = os.getenv("USERNAME_API")
    password = os.getenv("PASSWORD_API")

    token = await api.get_token(username, password)
    token = token.access_token

    checking = await check_user(tg_id)
    # print(checking)

    __expiry_timestamp = int(time.time()) + (days_sub * 86400)
    __expiry_timestamp * 1000

    if not data_limit == None:
        __data = data_limit * 2**30
    else:
        __data = 0

    if checking:
        update_user = UserModify(expire=__expiry_timestamp, data_limit=__data)
        await api.modify_user(tg_id, update_user, token)


async def get_days(chat_id: str):
    api = MarzbanAPI(api_url)
    username = os.getenv("USERNAME_API")
    password = os.getenv("PASSWORD_API")

    token = await api.get_token(username, password)
    token = token.access_token

    user = await api.get_user(chat_id, token)

    end_time = user.expire

      # Это время окончания подписки из БД
    current_time = int(time.time())  # Текущее время

    # Вычисляем количество оставшихся секунд
    remaining_seconds = max(end_time - current_time, 0)

    # Преобразуем секунды в дни
    remaining_days = remaining_seconds // 86400

    print(f"Осталось дней: {remaining_days}")
    return remaining_days