from extensions import db


turma_funcionarios = db.Table(
    "turma_funcionarios",
    db.Column("turma_id", db.Integer, db.ForeignKey("turmas.id"), primary_key=True),
    db.Column("funcionario_id", db.Integer, db.ForeignKey("funcionarios.id"), primary_key=True),
)


class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False, default="Turma")
    vagas = db.Column(db.Integer, nullable=False, default=20)
    data_inicio = db.Column(db.Date, nullable=True)
    data_fim = db.Column(db.Date, nullable=True)
    encerrada = db.Column(db.Boolean, nullable=False, default=False)
    treinamento_id = db.Column(db.Integer, db.ForeignKey("treinamentos.id"), nullable=False)

    treinamento = db.relationship("Treinamento", back_populates="turmas")
    funcionarios = db.relationship(
        "Funcionario",
        secondary=turma_funcionarios,
        back_populates="turmas",
    )

    @property
    def matriculados(self):
        return len(self.funcionarios)

    def __repr__(self):
        return f"<Turma {self.titulo} ({self.matriculados}/{self.vagas})>"
