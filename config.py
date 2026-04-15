from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
DATABASE_PATH = INSTANCE_DIR / "seloedu.db"

class Config:
    SECRET_KEY = "dev123"
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None