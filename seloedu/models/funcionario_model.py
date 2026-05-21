from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey
from extensions import db

class Funcionario(db.Model):
    __tablename__ = "funcionario"

    id_funcionario        = db.Column(db.Integer, primary_key=True)
    id_turma              = db.Column(db.Integer, db.ForeignKey("turma.id_turma"), nullable=False)
    nome                  = db.Column(db.String, nullable=False)
    email                  = db.Column(db.String, nullable=False)
    funcao                = db.Column(db.String, nullable=False)
    
    turma = db.relationship(
        "Turma",
        back_populates="funcionarios"
    )
