from flask import Blueprint
from flask_login import login_required
from views.treinamentos_views import (
    criar_turma,
    editar_treinamento,
    excluir_treinamento,
    excluir_turma,
    listar_treinamentos,
    detalhe_treinamento,
)


treinamento_bp = Blueprint("treinamento", __name__)

treinamento_bp.add_url_rule(
    "/treinamentos",
    view_func=login_required(listar_treinamentos),
    endpoint="listar",
    methods=["GET", "POST"],
)
treinamento_bp.add_url_rule(
    "/treinamentos/<int:id>/turmas/novo",
    view_func=login_required(criar_turma),
    endpoint="criar_turma",
    methods=["POST"],
)
treinamento_bp.add_url_rule(
    "/treinamentos/<int:id>",
    view_func=login_required(detalhe_treinamento),
    endpoint="detalhes",
    methods=["GET"],
)
treinamento_bp.add_url_rule(
    "/treinamentos/<int:id>/editar",
    view_func=login_required(editar_treinamento),
    endpoint="editar",
    methods=["GET", "POST"],
)
treinamento_bp.add_url_rule(
    "/treinamentos/<int:id>/excluir",
    view_func=login_required(excluir_treinamento),
    endpoint="excluir",
    methods=["POST"],
)
treinamento_bp.add_url_rule(
    "/turmas/<int:id>/excluir",
    view_func=login_required(excluir_turma),
    endpoint="excluir_turma",
    methods=["POST"],
)
