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