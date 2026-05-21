from flask import Blueprint
from flask_login import login_required

from views.funcionario_views import *

funcionarios_bp = Blueprint("funcionario", __name__)

funcionarios_bp.add_url_rule("/funcionario",          view_func=login_required(listar_funcionarios),  endpoint="listar",   methods=["GET"])
funcionarios_bp.add_url_rule("/funcionario/<int:id>", view_func=login_required(detalhes_funcionario), endpoint="detalhes", methods=["GET"])
funcionarios_bp.add_url_rule("/funcionario/modificar-funcionario/<int:id>", view_func=login_required(modificar_funcionario), endpoint="modificar", methods=["POST", "GET"])
funcionarios_bp.add_url_rule("/funcionario/deletar/<int:id>", view_func=login_required(detalhes_funcionario), endpoint="deletar", methods=["POST", "GET"])
funcionarios_bp.add_url_rule("/funcionario/criar/", view_func=login_required(criar_funcionario), endpoint="criar", methods=["POST", "GET"])
