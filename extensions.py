from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from config import Config


login_manager = LoginManager()
db = SQLAlchemy()
mail = Mail()
config = Config()


login_manager.login_view = "auth_login.login"
login_manager.login_message = "Faça login para acessar essa página."