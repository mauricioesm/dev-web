from datetime import datetime

from extensions import db


class Funcionario(db.Model):
    __tablename__ = "funcionarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(140), nullable=False, unique=True)
    cargo = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(30), nullable=True)
    status = db.Column(db.String(30), nullable=False, default="ativo")
    data_admissao = db.Column(db.Date, nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
