from py3xui import AsyncApi, Client
from py3xui.async_api import AsyncClientApi, AsyncInboundApi
from py3xui.inbound import Inbound, Settings, Sniffing, StreamSettings
from cryptography.hazmat.primitives.serialization import NoEncryption
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
# from handlers.cryptography_custom import *
from pprint import pprint
from logger import Logger
from os import getenv
import random
import base64
import uuid
import os


logger = Logger.getinstance()


async def create_inbound(name: str, chat_id: str, expire_time: int):
    username = getenv("USERNAME_API")
    password = getenv("PASSWORD_API")

    logger.info(f"username: {username}, pass: {password}")
    api = AsyncApi("http://150.241.85.190:32706/2SHzOV7jeAaM9DT", username, password)
    logger.info("пидорасы")
    await api.login()

    short_id = await generate_id()

    keys = generate_x25519_keys()

    settings = Settings(clients=[], decryption="none", fallbacks=[])
    sniffing = Sniffing(enabled=False)

    tcp_settings = {
        "acceptProxyProtocol": False,
        "header": {"type": "none"},
    }

    reality_settings = {
        "show": False,
        "dest": "google.com:443",  # Пример реального сервиса
        "xver": 0,
        "serverNames": ["google.com", "www.google.com"],
        "privateKey": keys[1],  # Сгенерировать ключи
        "minClient": "",
        "maxClient": "",
        "maxTimediff": 0,
        "shortIds": short_id,
        "settings": {
            "publicKey": keys[0],
            "fingerprint": "chrome",
            "serverName": "",
            "spiderX": "/",
        },
    }

    stream_settings = StreamSettings(
        security="reality",
        network="tcp",
        reality_settings=reality_settings,
        tcp_settings=tcp_settings,
    )

    import random

    port = random.randint(433, 9999)
    inbound = Inbound(
        enable=True,
        port=port,
        protocol="vless",
        settings=settings,
        stream_settings=stream_settings,
        sniffing=sniffing,
        remark=name,
    )

    await api.inbound.add(inbound)

    new_client = Client(
        id=str(uuid.uuid4()), email=chat_id, enable=True, expiryTime=expire_time
    )

    data_key = inbound.to_json()

    pprint(data_key["streamSettings"])


async def generate_id() -> list:
    # Длины сегментов в символах (из примера)
    segment_lengths = [16, 6, 8, 2, 12, 4, 10, 12]

    segments = []
    for _ in range(
        len(segment_lengths)
    ):  # Генерируем столько сегментов, сколько задано
        # Случайно выбираем длину сегмента
        length = random.choice(segment_lengths)

        # Вычисляем количество байт (1 символ hex = 4 бита)
        num_bytes = length // 2

        # Генерируем случайные байты
        random_bytes = os.urandom(num_bytes)

        # Конвертируем в HEX и добавляем в сегменты
        hex_segment = random_bytes.hex()
        segments.append(hex_segment)

    return segments
