from datetime import date
from extensions import db

turma_funcionarios = db.Table(
    "turma_funcionarios",
    db.Column("turma_id", db.Integer, db.ForeignKey("Turmas.id"), primary_key=True),
    db.Column("funcionario_id", db.Integer, db.ForeignKey("Funcionarios.id"), primary_key=True),
)


class Treinamento(db.Model):
    __tablename__ = "Treinamentos"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)
    turmas = db.relationship("Turma", back_populates="treinamento", cascade="all, delete-orphan")


class Turma(db.Model):
    __tablename__ = "Turmas"
    id = db.Column(db.Integer, primary_key=True)
    treinamento_id = db.Column(db.Integer, db.ForeignKey("Treinamentos.id"), nullable=False)
    vagas = db.Column(db.Integer, nullable=False, default=20)
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)
    treinamento = db.relationship("Treinamento", back_populates="turmas")
    funcionarios = db.relationship(
        "Funcionario", secondary=turma_funcionarios, back_populates="turmas"
    )

    @property
    def matriculados(self):
        return len(self.funcionarios)

    @property
    def lotada(self):
        return self.matriculados >= self.vagas

    @property
    def encerrada(self):
        return self.data_fim is not None and self.data_fim < date.today()
