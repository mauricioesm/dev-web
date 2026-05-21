from flask import Blueprint
from flask_login import login_required

from views.usuarios_views import *

usuarios_bp = Blueprint("usuario", __name__)

usuarios_bp.add_url_rule("/users",          view_func=login_required(listar_usuarios),  endpoint="listar",   methods=["GET"])
usuarios_bp.add_url_rule("/users/<int:id>", view_func=login_required(detalhes_usuario), endpoint="detalhes", methods=["GET"])
usuarios_bp.add_url_rule("/users/modificar-treinamento/<int:id>", view_func=login_required(modificar_usuario), endpoint="modificar", methods=["POST", "GET"])
usuarios_bp.add_url_rule("/users/deletar/<int:id>", view_func=login_required(deletar_usuario), endpoint="deletar", methods=["POST", "GET"])
usuarios_bp.add_url_rule("/users/criar/", view_func=login_required(criar_usuario), endpoint="criar", methods=["POST", "GET"])
