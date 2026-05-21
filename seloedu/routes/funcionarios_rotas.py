from flask import Blueprint
from flask_login import login_required

from views.funcionarios_views import (
    criar_funcionario,
    detalhes_funcionario,
    editar_funcionario,
    excluir_funcionario,
    listar_funcionarios,
)


funcionarios_bp = Blueprint("funcionarios", __name__, url_prefix="/funcionarios")

funcionarios_bp.add_url_rule("/", view_func=login_required(listar_funcionarios), endpoint="listar", methods=["GET"])
funcionarios_bp.add_url_rule("/novo", view_func=login_required(criar_funcionario), endpoint="criar", methods=["GET", "POST"])
funcionarios_bp.add_url_rule("/<int:id>", view_func=login_required(detalhes_funcionario), endpoint="detalhes", methods=["GET"])
funcionarios_bp.add_url_rule("/<int:id>/editar", view_func=login_required(editar_funcionario), endpoint="editar", methods=["GET", "POST"])
funcionarios_bp.add_url_rule("/<int:id>/excluir", view_func=login_required(excluir_funcionario), endpoint="excluir", methods=["POST"])
