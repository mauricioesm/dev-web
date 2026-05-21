from flask import Blueprint
from flask_login import login_required

from views.usuarios_views import (
    criar_usuario,
    detalhes_usuario,
    editar_usuario,
    excluir_usuario,
    listar_usuarios,
)

usuarios_bp = Blueprint("usuario", __name__)

usuarios_bp.add_url_rule("/users", view_func=login_required(listar_usuarios), endpoint="listar", methods=["GET"])
usuarios_bp.add_url_rule("/users/novo", view_func=login_required(criar_usuario), endpoint="criar", methods=["GET", "POST"])
usuarios_bp.add_url_rule("/users/<int:id>", view_func=login_required(detalhes_usuario), endpoint="detalhes", methods=["GET"])
usuarios_bp.add_url_rule("/users/<int:id>/editar", view_func=login_required(editar_usuario), endpoint="editar", methods=["GET", "POST"])
usuarios_bp.add_url_rule("/users/<int:id>/excluir", view_func=login_required(excluir_usuario), endpoint="excluir", methods=["POST"])
