from py3xui import AsyncApi, Client, Inbound
from logger import Logger
from os import getenv
import secrets
import pyqrcode
import uuid
import time

logger = Logger.getinstance()



async def create_user_vpn(name: str, days_valid: int) -> uuid.uuid4:
    username = getenv("USERNAME_API")
    password = getenv("PASSWORD_API")

    expiry_timestamp = int(time.time()) + (days_valid * 86400)
    expiry_timestamp * 1000

    logger.info(f"username: {username}, pass: {password}")
    api = AsyncApi("http://150.241.85.190:32706/2SHzOV7jeAaM9DT", username, password)
    await api.login()

    client_uuid = str(uuid.uuid4())

    client = Client(
        id=client_uuid, email=name, enable=True, expiryTime=expiry_timestamp * 1000
    )

    # print(client)
    # inbound = await api.inbound.get_by_id(2)
    # print(inbound.settings.clients[0])

    await api.client.add(2, [client])

    return client_uuid

async def update_user(client_id: str, days_valid: int):
    username = getenv("USERNAME_API")
    password = getenv("PASSWORD_API")

    # logger.info(f"username: {username}, pass: {password}")
    api = AsyncApi("http://150.241.85.190:32706/2SHzOV7jeAaM9DT", username, password)
    await api.login()

    expiry_timestamp = int(time.time()) + (days_valid * 86400)
    expiry_timestamp * 1000

    client = await api.client.get_by_email("Timur")
    inbound = await api.inbound.get_by_id(2)

    # print(client)
    # print(inbound.settings.clients[0])

    # await api.client.delete(2, inbound.settings.clients[0].id)

def get_connection_string(inbound: Inbound, user_uuid: str, user_email) -> str:
    """Prepare a connection string for the given inbound, user UUID and telegram ID.

    Arguments:
        inbound (Inbound): The inbound object.
        user_uuid (str): The UUID of the user.
        user_email (int): The email of the user.

    Returns:
        str: The connection string.
    """

    XUI_EXTERNAL_IP=getenv("API_URL")
    MAIN_REMARK='Kitty_vpn'

    public_key = inbound.stream_settings.reality_settings.get("settings").get("publicKey")
    logger.info(public_key)
    website_name = inbound.stream_settings.reality_settings.get("serverNames")[0]
    logger.info(website_name)
    short_id = inbound.stream_settings.reality_settings.get("shortIds")[0]
    logger.info(short_id)

    connection_string = (
        f"vless://{user_uuid}@{XUI_EXTERNAL_IP}"
        f"?type=tcp&security=reality&pbk={public_key}&fp=firefox&sni={website_name}"
        f"&sid={short_id}&spx=%2F#{MAIN_REMARK}-{user_email}"
    )

    return connection_string