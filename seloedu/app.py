import secrets
from pathlib import Path
from flask import Flask, redirect, render_template, session, url_for
from flask_login import current_user, login_required, logout_user
from config import Config
from extensions import db, login_manager, mail
from models.funcionario_model import Funcionario
from models.treinamento_model import Treinamento
from models.turma_model import Turma
from models.usuario_models import Usuario

from routes.auth_rotas import auth_bp
from routes.dashboard_rotas import dashboard_bp
from routes.funcionarios_rotas import funcionarios_bp
from routes.treinamentos_rotas import treinamentos_bp
from routes.turmas_rotas import turmas_bp
from routes.usuarios_rotas import usuarios_bp


app = Flask(__name__)
Path(app.instance_path).mkdir(parents=True, exist_ok=True)
app.config.from_object(Config)
app.config["APP_RUN_ID"] = secrets.token_hex(16)

db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(funcionarios_bp)
app.register_blueprint(treinamentos_bp)
app.register_blueprint(turmas_bp)
app.register_blueprint(usuarios_bp)


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(Usuario, int(user_id))
    except (TypeError, ValueError):
        return None

@app.before_request
def expire_session_after_restart():
    if not current_user.is_authenticated:
        return None

    if session.get("app_run_id") == app.config["APP_RUN_ID"]:
        return None

    logout_user()
    session.clear()
    return None

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/home")
@login_required
def home_alias():
    return redirect(url_for("dashboard.index"))

@app.route("/entrar")
def login_alias():
    return redirect(url_for("auth.login"))

with app.app_context():
    db.create_all()
    if not Usuario.query.filter_by(email="admin@seloedu.com").first():
        master = Usuario(
            nome="Admin Master",
            email="admin@seloedu.com",
            funcao="master",
        )
        master.set_password("123456")
        db.session.add(master)
        db.session.commit()

if __name__ == "__main__":
    #app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)
