from py3xui import AsyncApi, Client
from py3xui.async_api import AsyncClientApi, AsyncInboundApi
from py3xui.inbound import Inbound, Settings, Sniffing, StreamSettings
from cryptography.hazmat.primitives.serialization import NoEncryption
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from decouple import config
import base64
import uuid

username = config("USERNAME_API")
password = config("PASSWORD_API")

# === Генерация ключей для REALITY ===
private_key = ed25519.Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# Кодируем публичный ключ в формат base64 (как в VLESS)
pbk = base64.urlsafe_b64encode(public_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
)).decode().rstrip("=")

prvk = base64.urlsafe_b64encode(private_key.private_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PrivateFormat.Raw,
    encryption_algorithm=NoEncryption()
)).decode().rstrip("=")

# prvk = private_key.private_bytes(
#     encoding=serialization.Encoding.Raw,
#     format=serialization.PrivateFormat.Raw,
#     encryption_algorithm=NoEncryption()
# ).decode(errors='replace').rstrip("=")

# print(pbk)
# print(prvk)

api = AsyncApi("http://150.241.85.190:54321/1xQjW5L8tD2dnXE/", username, password)

async def create_inbound(name: str, chat_id: str, expire_time: int):
    await api.login()


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
            "serverNames": ["google.com"],
            "publicKey": pbk,
            "privateKey": prvk,  # Сгенерировать ключи
            "minClient": "",
            "maxClient": "",
            "maxTimediff": 0,
            "shortIds": ["abcd1234"]
    }

    stream_settings = StreamSettings(security="reality", 
                                     network="tcp", 
                                     reality_settings=reality_settings,
                                     tcp_settings=tcp_settings)

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
  
    new_client = Client(id=str(uuid.uuid4()), email=chat_id, enable=True, expiryTime=expire_time)

    # await api.client.add(inbound_id, [new_client])
    
async def main():
    inbound_id = await create_inbound('bebra123', 'bebrus1123@mail.com', 23232323)
    print(inbound_id)

import asyncio

asyncio.run(main())