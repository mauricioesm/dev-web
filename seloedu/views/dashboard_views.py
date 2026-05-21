from flask import render_template

from models.funcionario_model import Funcionario
from models.treinamento_model import Treinamento
from models.turma_model import Turma
from models.usuario_models import Usuario


def dashboard():
    cards = [
        ("Funcionarios", Funcionario.query.count(), "Cadastros internos"),
        ("Treinamentos", Treinamento.query.count(), "Programas cadastrados"),
        ("Turmas", Turma.query.filter_by(ativo=True).count(), "Turmas ativas no painel"),
        ("Usuarios", Usuario.query.count(), "Acessos administrativos"),
    ]

    treinamentos = (
        Treinamento.query.order_by(Treinamento.data_criacao.desc()).limit(5).all()
    )
    turmas = (
        Turma.query.filter_by(ativo=True)
        .order_by(Turma.criado_em.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard/dashboard.html",
        cards=cards,
        treinamentos=treinamentos,
        turmas=turmas,
    )
