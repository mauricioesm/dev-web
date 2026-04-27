from flask import Blueprint
from flask_login import login_required

from views.usuarios_views import detalhes_usuario, listar_usuarios

usuarios_bp = Blueprint("usuario", __name__)

usuarios_bp.add_url_rule("/users",          view_func=login_required(listar_usuarios),  endpoint="listar",   methods=["GET"])
usuarios_bp.add_url_rule("/users/<int:id>", view_func=login_required(detalhes_usuario), endpoint="detalhes", methods=["GET"])
