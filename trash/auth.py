import requests

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
check_url = "http://176.124.202.220:61247/SMs3hwMea8PbV0q/panel/api/inbounds/list"

def get_auth_token(host: str, port: int, username: str, password: str) -> str:
    # 1. Авторизация

    payload = {
        "up": 0,
        "down": 0,
        "total": 0,
        "remark": "test",  # Имя пользователя
        "enable": True,
        "expiryTime": 0,  # Переводим в миллисекунды
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

        # 3. Проверяем список ключей
        check_response = requests.get(check_url, headers=headers)
        print("Список ключей:", check_response.status_code)

    else:
        print("Ошибка авторизации:", login_response.text)


# Пример использования
host = "176.124.202.220"
port = 54321
username = "7dkAvyu8vB"
password = "sBqFiU1hwz"

token = get_auth_token(host, port, username, password)
if token:
    print("Токен:", token)
