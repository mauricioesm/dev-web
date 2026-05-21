from flask import Blueprint
from flask_login import login_required

from views.turmas_views import *

turmas_bp = Blueprint("turma", __name__)

turmas_bp.add_url_rule("/turmas",          view_func=login_required(listar_turma),  endpoint="listar",   methods=["GET"])
turmas_bp.add_url_rule("/turmas/<int:id>", view_func=login_required(detalhes_turma), endpoint="detalhes", methods=["GET"])
turmas_bp.add_url_rule("/turmas/modificar-treinamento/<int:id>", view_func=login_required(modificar_turma), endpoint="modificar", methods=["POST", "GET"])
turmas_bp.add_url_rule("/turmas/deletar/<int:id>", view_func=login_required(deletar_turma), endpoint="deletar", methods=["POST", "GET"])
turmas_bp.add_url_rule("/turmas/criar/", view_func=login_required(criar_turma), endpoint="criar", methods=["POST", "GET"])
