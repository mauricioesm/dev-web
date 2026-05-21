from datetime import datetime

from extensions import db


class Treinamento(db.Model):
    __tablename__ = "treinamentos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(140), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    carga_horaria = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(30), nullable=False, default="ativo")
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    turmas = db.relationship(
        "Turma",
        back_populates="treinamento",
        cascade="all, delete-orphan",
    )
