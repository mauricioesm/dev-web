<<<<<<< HEAD
import secrets
from pathlib import Path

class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///seloedu.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

=======
import secrets
from pathlib import Path

class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///seloedu.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

>>>>>>> 6683954228eabc2f7059abea721c978659899293
