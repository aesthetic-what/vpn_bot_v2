from py3xui import AsyncApi, Client
from logger import Logger
from os import getenv
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

    await api.client.add(2, [client])
    # key_str = await get_connection_string(client_uuid, name)
    # return key_str, client_uuid, expiry_timestamp

async def get_connection_string(user_uuid: str, user_email) -> str:
    """Prepare a connection string for the given inbound, user UUID and telegram ID.

    Arguments:
        inbound (Inbound): The inbound object.
        user_uuid (str): The UUID of the user.
        user_email (int): The email of the user.

    Returns:
        str: The connection string.
    """

    username = getenv("USERNAME_API")
    password = getenv("PASSWORD_API")

    # logger.info(f"username: {username}, pass: {password}")
    api = AsyncApi("http://150.241.85.190:32706/2SHzOV7jeAaM9DT", username, password)
    await api.login()
    # 3️⃣ Get the inbound.
    inbound = await api.inbound.get_by_id(2)
    print(f"Inbound has {len(inbound.settings.clients)} clients")

    XUI_EXTERNAL_IP=getenv("EXTERNAL_URL")
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

    # print(connection_string)
    return connection_string

async def update_client_key(name: str):

    username = getenv("USERNAME_API")
    password = getenv("PASSWORD_API")

    api = AsyncApi("http://150.241.85.190:32706/2SHzOV7jeAaM9DT", username, password)
    await api.login()
    # 3️⃣ Get the inbound.
    inbound = await api.inbound.get_by_id(2)
    logger.info(f"Inbound has {len(inbound.settings.clients)} clients")

    # 4️⃣ Find the needed client in the inbound.
    client = None
    for c in inbound.settings.clients:
        if c.email == name:
            client = c
            break

    if client:
        print(f"Found client with ID: {client.id}")  # ⬅️ The actual Client UUID.
    else:
        raise ValueError(f"Client with email {name} not found")

    cliend_uuid = client.id
    logger.info(cliend_uuid)

    for c in inbound.settings.clients:
        print(f"clients email: {c.email}")

    test = await api.client.get_ips(name)
    print(test)