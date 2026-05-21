from flask import Blueprint
from flask_login import login_required

from views.treinamentos_views import *

treinamentos_bp = Blueprint("treinamento", __name__)

treinamentos_bp.add_url_rule("/treinamentos",          view_func=login_required(listar_treinamento),  endpoint="listar",   methods=["GET"])
treinamentos_bp.add_url_rule("/treinamentos/<int:id>", view_func=login_required(detalhes_treinamento), endpoint="detalhes", methods=["GET"])
treinamentos_bp.add_url_rule("/treinamentos/modificar-treinamento/<int:id>", view_func=login_required(modificar_treinamento), endpoint="modificar", methods=["POST", "GET"])
treinamentos_bp.add_url_rule("/treinamentos/deletar/<int:id>", view_func=login_required(detalhes_treinamento), endpoint="deletar", methods=["POST", "GET"])
treinamentos_bp.add_url_rule("/treinamentos/criar/", view_func=login_required(criar_treinamento), endpoint="criar", methods=["POST", "GET"])
