from datetime import datetime

from extensions import db


class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    treinamento_id = db.Column(
        db.Integer,
        db.ForeignKey("treinamentos.id"),
        nullable=False,
    )
    vagas = db.Column(db.Integer, nullable=False, default=20)
    data_inicio = db.Column(db.Date, nullable=True)
    data_fim = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30), nullable=False, default="planejada")
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    treinamento = db.relationship("Treinamento", back_populates="turmas")
