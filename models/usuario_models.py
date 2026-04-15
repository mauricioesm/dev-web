from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from datetime import datetime, timedelta
import secrets

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    senha_hash = db.Column(db.String(225), nullable=False)
    funcao = db.Column(db.String(50), nullable=False, default="coordenador")
    reset_token = db.Column(db.String(100), nullable=True)
    reset_expiry = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)

    def get_reset_token(self):
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_expiry = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token

    def verify_reset_token(self, token):
        return self.reset_token == token and self.reset_expiry > datetime.utcnow()