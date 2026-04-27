from flask import Blueprint
from flask_login import login_required

from views.usuarios_views import (
    detalhes_usuario,
    listar_usuarios,
    criar_usuario,
    editar_usuario,
    deletar_usuario,
)

usuarios_bp = Blueprint("usuario", __name__)

usuarios_bp.add_url_rule("/users", view_func=login_required(listar_usuarios), endpoint="listar", methods=["GET"])
usuarios_bp.add_url_rule("/users/create", view_func=criar_usuario, endpoint="criar", methods=["GET", "POST"])
usuarios_bp.add_url_rule("/users/<int:id>", view_func=login_required(detalhes_usuario), endpoint="detalhes", methods=["GET"])
usuarios_bp.add_url_rule("/users/<int:id>/edit", view_func=login_required(editar_usuario), endpoint="editar", methods=["GET", "POST"])
usuarios_bp.add_url_rule("/users/<int:id>/delete", view_func=login_required(deletar_usuario), endpoint="deletar", methods=["POST"])
