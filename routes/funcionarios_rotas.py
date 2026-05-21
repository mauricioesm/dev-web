from flask import Blueprint
from flask_login import login_required
from views.funcionarios_views import (
    detalhes_funcionario,
    listar_funcionarios,
    criar_funcionario,
    excluir_funcionario,
    editar_funcionario,
)


funcionario_bp = Blueprint("funcionario", __name__)

funcionario_bp.add_url_rule(
    "/funcionarios",
    view_func=login_required(listar_funcionarios),
    endpoint="listar",
    methods=["GET", "POST"],
)
funcionario_bp.add_url_rule(
    "/funcionarios/novo",
    view_func=login_required(criar_funcionario),
    endpoint="novo",
    methods=["POST"],
)
funcionario_bp.add_url_rule(
    "/funcionarios/<int:id>",
    view_func=login_required(detalhes_funcionario),
    endpoint="detalhes",
    methods=["GET"],
)
funcionario_bp.add_url_rule(
    "/funcionarios/<int:id>/editar",
    view_func=login_required(editar_funcionario),
    endpoint="editar",
    methods=["GET", "POST"],
)
funcionario_bp.add_url_rule(
    "/funcionarios/<int:id>/excluir",
    view_func=login_required(excluir_funcionario),
    endpoint="excluir",
    methods=["POST"],
)
