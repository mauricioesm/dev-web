from extensions import db


class Treinamento(db.Model):
    __tablename__ = "treinamentos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data_inicio = db.Column(db.Date, nullable=True)
    data_fim = db.Column(db.Date, nullable=True)
    local = db.Column(db.String(120), nullable=True)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    turmas = db.relationship("Turma", back_populates="treinamento", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Treinamento {self.titulo}>"
