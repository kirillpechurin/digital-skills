import os

from dotenv import load_dotenv

load_dotenv()

# HTTP Server
HTTP_HOST = os.getenv("HTTP_HOST")
HTTP_PORT = int(os.getenv("HTTP_PORT"))
DEBUG = bool(int(os.getenv("DEBUG")))

# Database
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Email
MAIL_HOST = os.getenv("MAIL_HOST")
MAIL_PORT = int(os.getenv("MAIL_PORT"))
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

# Additional
SECRET_KEY_SESSION = os.getenv("SECRET_KEY_SESSION")
SECRET_KEY = os.getenv("SECRET_KEY")
ENCRYPT_ALGORITHM = os.getenv("ENCRYPT_ALGORITHM")
LIFETIME_CODE = int(os.getenv("LIFETIME_CODE"))
SEND_CODE_INTERVAL = int(os.getenv("SEND_CODE_INTERVAL"))
