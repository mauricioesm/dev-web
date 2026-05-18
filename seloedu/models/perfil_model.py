from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey
from extensions import db

class Perfil(db.Model):
    __tablename__ ="perfis"
    id = db.Column(db.Integer, primary_key=True)
    telefone = db.Column(db.String(11), nullable=True)
    instituicao = db.Column(db.String(100), nullable=True)
    cargo = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.String(100), nullable=True)
    foto = db.Column(db.String(200), nullable=True)
    foto_thumb = db.Column(db.String(200), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True, nullable=False)

    usuario = db.relationship(
        'Usuario',
        back_populates='perfil', 
        uselist=False
    )
