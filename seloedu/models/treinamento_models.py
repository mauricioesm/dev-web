from extensions import db

turma_funcionario = db.Table('turma_funcionario',
    db.Column('turma_id', db.Integer, db.ForeignKey('turmas.id'), primary_key=True),
    db.Column('funcionario_id', db.Integer, db.ForeignKey('funcionarios.id'), primary_key=True)
)

class Funcionario(db.Model):
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Treinamento(db.Model):
    __tablename__ = 'treinamentos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    data_inicio = db.Column(db.Date, nullable=True)
    data_fim = db.Column(db.Date, nullable=True)
    
    turmas = db.relationship('Turma', backref='treinamento', cascade="all, delete-orphan", lazy=True)

class Turma(db.Model):
    __tablename__ = 'turmas'
    id = db.Column(db.Integer, primary_key=True)
    treinamento_id = db.Column(db.Integer, db.ForeignKey('treinamentos.id'), nullable=False)
    vagas = db.Column(db.Integer, nullable=False, default=20)
    data_inicio = db.Column(db.Date, nullable=True)
    data_fim = db.Column(db.Date, nullable=True)
    
    funcionarios = db.relationship('Funcionario', secondary=turma_funcionario, backref=db.backref('turmas', lazy=True))

    @property
    def matriculados(self):
        return len(self.funcionarios)