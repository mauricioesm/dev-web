from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey
from extensions import db

class Treinamento(db.Model):
    __tablename__ = "treinamento"

    id_treinamento      = db.Column(db.Integer, primary_key=True)
    disciplina          = db.Column(db.String, nullable=False)
    carga_horaria       = db.Column(db.Integer, nullable=False)
    capacidade          = db.Column(db.Integer, nullable=False)

    turmas = db.relationship(
        "Turma",
        back_populates="treinamentos"
    )