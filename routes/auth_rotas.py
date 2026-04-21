from flask import Blueprint
from views.auth_views import login, send_test_email, esqueci_senha, redefinir_senha

auth_login = Blueprint("auth_login", __name__, template_folder='templates')


auth_login.add_url_rule('/login', methods=['GET', 'POST'], view_func=login)

auth_login.add_url_rule('/send_test_email', view_func=send_test_email)

auth_login.add_url_rule('/esqueceu-senha', methods=['GET','POST'], view_func=esqueci_senha)

auth_login.add_url_rule('/redefinir-senha/<token>', methods=['GET','POST'], view_func=redefinir_senha)