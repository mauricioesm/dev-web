from flask import Blueprint
from flask_login import login_required

from views.treinamentos_views import (
    criar_treinamento,
    detalhes_treinamento,
    editar_treinamento,
    excluir_treinamento,
    listar_treinamentos,
)


treinamentos_bp = Blueprint("treinamentos", __name__, url_prefix="/treinamentos")

treinamentos_bp.add_url_rule("/", view_func=login_required(listar_treinamentos), endpoint="listar", methods=["GET"])
treinamentos_bp.add_url_rule("/novo", view_func=login_required(criar_treinamento), endpoint="criar", methods=["GET", "POST"])
treinamentos_bp.add_url_rule("/<int:id>", view_func=login_required(detalhes_treinamento), endpoint="detalhes", methods=["GET"])
treinamentos_bp.add_url_rule("/<int:id>/editar", view_func=login_required(editar_treinamento), endpoint="editar", methods=["GET", "POST"])
treinamentos_bp.add_url_rule("/<int:id>/excluir", view_func=login_required(excluir_treinamento), endpoint="excluir", methods=["POST"])
