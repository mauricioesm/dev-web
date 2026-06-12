from extensions import db
from models.treinamento_models import turma_funcionarios


class Funcionario(db.Model):
    __tablename__ = "Funcionarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cargo = db.Column(db.String(100), nullable=False, default="colaborador")
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    turmas = db.relationship(
        "Turma", secondary=turma_funcionarios, back_populates="funcionarios"
    )
