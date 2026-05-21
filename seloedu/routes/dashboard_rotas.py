from flask import Blueprint
from flask_login import login_required

from views.dashboard_views import dashboard


dashboard_bp = Blueprint("dashboard", __name__)

dashboard_bp.add_url_rule(
    "/dashboard",
    view_func=login_required(dashboard),
    endpoint="index",
    methods=["GET"],
)
