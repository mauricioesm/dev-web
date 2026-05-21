from extensions import db


class Funcionario(db.Model):
    __tablename__ = "funcionarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cargo = db.Column(db.String(120), nullable=True)
    telefone = db.Column(db.String(40), nullable=True)

    turmas = db.relationship(
        "Turma",
        secondary="turma_funcionarios",
        back_populates="funcionarios",
    )

    def __repr__(self):
        return f"<Funcionario {self.nome} ({self.email})>"
