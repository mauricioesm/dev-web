from flask import Blueprint
from flask_login import login_required

from views.turmas_views import criar_turma, editar_turma, excluir_turma, listar_turmas


turmas_bp = Blueprint("turmas", __name__, url_prefix="/turmas")

turmas_bp.add_url_rule("/", view_func=login_required(listar_turmas), endpoint="listar", methods=["GET"])
turmas_bp.add_url_rule("/novo", view_func=login_required(criar_turma), endpoint="criar", methods=["GET", "POST"])
turmas_bp.add_url_rule("/<int:id>/editar", view_func=login_required(editar_turma), endpoint="editar", methods=["GET", "POST"])
turmas_bp.add_url_rule("/<int:id>/excluir", view_func=login_required(excluir_turma), endpoint="excluir", methods=["POST"])
