from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey
from extensions import db

class Turma(db.Model):
    __tablename__ = "turma"

    id_turma         = db.Column(db.Integer, primary_key=True)
    id_treinamento   = db.Column(db.Integer, db.ForeignKey("treinamento.id_treinamento"), nullable=False)
    qtd_funcionarios = db.Column(db.Integer, nullable=False)

    funcionarios = db.relationship (
        "Funcionario",
        back_populates="turma"
    )

    treinamentos = db.relationship (
        "Treinamento",
        back_populates="turmas",
        uselist=False
    )




