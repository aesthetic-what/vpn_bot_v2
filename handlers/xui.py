from py3xui import AsyncApi, Client
from py3xui.async_api import AsyncClientApi, AsyncInboundApi
from py3xui.inbound import Inbound, Settings, Sniffing, StreamSettings
from decouple import config
import uuid

username = config("USERNAME_API")
password = config("PASSWORD_API")

api = AsyncApi("http://176.124.202.220:61247/SMs3hwMea8PbV0q/", username, password)

async def create_inbound(name: str, chat_id: str, expire_time: int):
    await api.login()


    settings = Settings()
    sniffing = Sniffing(enabled=False)

    tcp_settings = {
    "acceptProxyProtocol": False,
    "header": {"type": "none"},
    }

    stream_settings = StreamSettings(security="reality", network="tcp", tcp_settings=tcp_settings)

    inbound = Inbound(
        enable=True,
        port=443,
        protocol="vless",
        settings=settings,
        stream_settings=stream_settings,
        sniffing=sniffing,
        remark=name,
    )

    await api.inbound.add(inbound)

    inbound_id = inbound.id

    await create_user(inbound_id, chat_id, expire_time)

async def create_user(inbound_id: int, chat_id: str | int, expire_time: int):
    await api.login()

    new_client = Client(id=str(uuid.uuid4()), email=chat_id, enable=True, expiryTime=expire_time)

    await api.client.add(inbound_id, [new_client])