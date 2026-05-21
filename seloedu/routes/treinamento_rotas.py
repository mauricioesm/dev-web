from flask import Blueprint
from flask_login import login_required
from views.treinamento_views import listar_treinamentos

treinamentos_bp = Blueprint("treinamentos", __name__)

treinamentos_bp.add_url_rule("/treinamentos", view_func=login_required(listar_treinamentos), endpoint="listar", methods=["GET", "POST"])