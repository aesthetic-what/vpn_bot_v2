import uuid
import time
import secrets
import base64
import pyqrcode
import requests
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

# === Конфигурация VPN-сервера ===
server = "176.124.202.220"  # IP-адрес или домен
port = 443  # Порт сервера
security = "reality"  # Тип шифрования (none, tls, reality)
network = "tcp"  # Протокол (tcp, ws, grpc)
sni = "google.com"  # Домен для маскировки (SNI)
fingerprint = "chrome"  # Маскировка под браузер
api_port = 5252
username = ""
password = ""
api_url = f"http://176.124.202.220:61247/SMs3hwMea8PbV0q/panel/api/inbounds/add"
login_url = "http://176.124.202.220:61247/SMs3hwMea8PbV0q/login"

async def add_to_serever(user_uuid, name, expiry_timestamp):
    session = requests.Session()
    payload = {
        "up": 0,
        "down": 0,
        "total": 0,
        "remark": name,  # Имя пользователя
        "enable": True,
        "expiryTime": expiry_timestamp * 1000,  # Переводим в миллисекунды
        "listen": "",
        "port": 443,  # Порт Xray
        "protocol": "vless",
        "settings": {
            "clients": [
                {
                "id": "fd95d112-dd17-4a1e-9f4b-d105eabb29b3",
                "flow": "xtls-rprx-vision",
                "email": "8nz67r2e",
                "limitIp": 0,
                "totalGB": 0,
                "expiryTime": 0,
                "enable": True,
                "tgId": "",
                "subId": "u67g6uvr1pumx7j0",
                "comment": "",
                "reset": 0
                }
            ],
            "decryption": "none",
            "fallbacks": []
        },
        "streamSettings": {
            "network": "tcp",
            "security": "reality",
            "externalProxy": [],
            "realitySettings": {
                "show": False,
                "xver": 0,
                "dest": "google.com:443",
                "serverNames": [
                "google.com",
                "www.google.com"
                ],
                "privateKey": "iHfFpnMoUo1yFR7idy0ZNoswsucAw12tdgNBecDRMkI",
                "minClient": "",
                "maxClient": "",
                "maxTimediff": 0,
                "shortIds": [
                "0562",
                "6a1483",
                "a0d942abe2ba",
                "bf",
                "5f32fdaf123eb0",
                "fee76280f0c03416",
                "f8f35550a4",
                "cd515ded"
                ],
                "settings": {
                "publicKey": "52cP-KMR1LHeFDQTwypRpk68KdtCT5A9uPfIKFUSdGM",
                "fingerprint": "chrome",
                "serverName": "",
                "spiderX": "/"
                }
            },
            "tcpSettings": {
                "acceptProxyProtocol": False,
                "header": {
                "type": "none"
                }
            }
        },
        "sniffing": {
            "enabled": False,
            "destOverride": [
                "http",
                "tls",
                "quic",
                "fakedns"
            ],
            "metadataOnly": False,
            "routeOnly": False
            },
        "allocate": {
            "strategy": "always",
            "refresh": 5,
            "concurrency": 3
            }
    }

    headers = {"Content-Type": "application/json"}
    data = {"username": username, "password": password}
    login_response = requests.post(login_url, json=data)

    if login_response.status_code == 200 and "obj" in login_response.json():
        token = "MTc0MDYwMjI4NnxEWDhFQVFMX2dBQUJFQUVRQUFCMV80QUFBUVp6ZEhKcGJtY01EQUFLVEU5SFNVNWZWVk5GVWhoNExYVnBMMlJoZEdGaVlYTmxMMjF2WkdWc0xsVnpaWExfZ1FNQkFRUlZjMlZ5QWYtQ0FBRUVBUUpKWkFFRUFBRUlWWE5sY201aGJXVUJEQUFCQ0ZCaGMzTjNiM0prQVF3QUFRdE1iMmRwYmxObFkzSmxkQUVNQUFBQUh2LUNHd0VDQVFvM1pHdEJkbmwxT0haQ0FRcHpRbkZHYVZVeGFIZDZBQT09fLn4_s-LeyMRc2eCkjHw_ouwLkgZS17qT-f9tqMIIWJt"  # Получаем токен
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Добавляем ключ
        add_key_response = requests.post(api_url, json=payload, headers=headers)
        print("Добавление ключа:", add_key_response.status_code)

    else:
        print("Ошибка авторизации:", login_response.text)

async def generate_qrcode(name: str | int, days_valid: int):
    # === Генерация ключей для REALITY ===
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Кодируем публичный ключ в формат base64 (как в VLESS)
    pbk = base64.urlsafe_b64encode(public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )).decode().rstrip("=")

    # === Генерация UUID пользователя ===
    user_uuid = str(uuid.uuid4())

    # === Генерация Session ID (SID) ===
    sid = secrets.token_hex(6)  # 6 байт -> 12 символов

    # === Устанавливаем срок подписки (например, 30 дней) ===
    expiry_timestamp = int(time.time()) + (days_valid * 86400)  # Текущее время + 30 дней

    # === Генерация VLESS-ссылки ===
    vless_url = (f"vless://{user_uuid}@{server}:{port}?"
                f"type={network}&security={security}&pbk={pbk}"
                f"&fp={fingerprint}&sni={sni}&sid={sid}&spx=%2F&exp={expiry_timestamp}#{name}")

    await add_to_serever(user_uuid=user_uuid, name=name, expiry_timestamp=expiry_timestamp)
    # print("Ваш VLESS-ключ:")
    # print(vless_url)

    # === Дата истечения подписки в читаемом формате ===
    expiry_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(expiry_timestamp))
    print(f"Срок подписки истекает: {expiry_date}")

    qrcode = pyqrcode.create(content=vless_url, error="Q", version=13, mode='binary', encoding='utf-8')
    image_qr = qrcode.png('qr_code.png', scale=5)
    return vless_url

import asyncio
test = asyncio.run(generate_qrcode('test_name', 60))
print(test)