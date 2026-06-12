from flask import Blueprint
from flask_login import login_required
from views.treinamentos_views import (
    editar_treinamento,
    excluir_treinamento,
    listar_treinamentos,
    novo_treinamento,
)

treinamentos_bp = Blueprint("treinamento", __name__)

treinamentos_bp.add_url_rule(
    "/treinamentos",
    view_func=login_required(listar_treinamentos),
    endpoint="listar",
    methods=["GET"],
)
treinamentos_bp.add_url_rule(
    "/treinamentos/novo",
    view_func=login_required(novo_treinamento),
    endpoint="novo",
    methods=["GET", "POST"],
)
treinamentos_bp.add_url_rule(
    "/treinamentos/<int:id>/editar",
    view_func=login_required(editar_treinamento),
    endpoint="editar",
    methods=["GET", "POST"],
)
treinamentos_bp.add_url_rule(
    "/treinamentos/<int:id>/excluir",
    view_func=login_required(excluir_treinamento),
    endpoint="excluir",
    methods=["POST"],
)
