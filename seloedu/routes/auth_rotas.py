from flask import Blueprint
from views.auth_views import auth as auth_view

auth_bp = Blueprint("auth", __name__)

auth_bp.add_url_rule("/login",  view_func=auth_view.login,  endpoint="login",  methods=["GET", "POST"])
auth_bp.add_url_rule("/logout", view_func=auth_view.logout, endpoint="logout", methods=["GET"])
auth_bp.add_url_rule(
    "/esqueci-senha",
    view_func=auth_view.forgot_password,
    endpoint="forgot_password",
    methods=["GET", "POST"],
)
auth_bp.add_url_rule(
    "/redefinir-senha",
    view_func=auth_view.reset_password,
    endpoint="reset_password",
    methods=["GET", "POST"],
)
