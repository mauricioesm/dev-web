import secrets
from datetime import date
from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, logout_user
from config import Config
from extensions import db, login_manager, mail
from models.usuario_models import Usuario
from models.treinamento_models import Treinamento, Turma
from models.funcionario_models import Funcionario
from routes.auth_rotas import auth_bp
from routes.usuarios_rotas import usuarios_bp
from routes.treinamentos_rotas import treinamentos_bp

app = Flask(__name__)
Path(app.instance_path).mkdir(parents=True, exist_ok=True)
app.config.from_object(Config)
app.config["APP_RUN_ID"] = secrets.token_hex(16)

db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(treinamentos_bp)


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(Usuario, int(user_id))
    except (TypeError, ValueError):
        return None


@app.before_request
def expire_session_after_restart():
    if not current_user.is_authenticated:
        return
    if session.get("app_run_id") != app.config["APP_RUN_ID"]:
        logout_user()
        session.clear()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/home")
@login_required
def home_alias():
    return redirect(url_for("dashboard_alias"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard_alias():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "create_turma":
            treinamento_id = request.form.get("treinamento_id", type=int)
            vagas = request.form.get("vagas", type=int) or 20
            data_inicio_str = request.form.get("data_inicio", "")
            data_fim_str = request.form.get("data_fim", "")
            turma = Turma(
                treinamento_id=treinamento_id,
                vagas=vagas,
                data_inicio=date.fromisoformat(data_inicio_str) if data_inicio_str else None,
                data_fim=date.fromisoformat(data_fim_str) if data_fim_str else None,
            )
            db.session.add(turma)
            db.session.commit()
            return redirect(url_for("dashboard_alias", treinamento_id=treinamento_id))

        if action == "delete_turma":
            turma_id = request.form.get("turma_id", type=int)
            turma = db.session.get(Turma, turma_id)
            if turma:
                treinamento_id = turma.treinamento_id
                db.session.delete(turma)
                db.session.commit()
                return redirect(url_for("dashboard_alias", treinamento_id=treinamento_id))
            return redirect(url_for("dashboard_alias"))

        if action == "add_funcionario":
            turma_id = request.form.get("turma_id", type=int)
            funcionario_id = request.form.get("funcionario_id", type=int)
            turma = db.session.get(Turma, turma_id)
            funcionario = db.session.get(Funcionario, funcionario_id)
            if turma and funcionario and not turma.lotada and not turma.encerrada:
                turma.funcionarios.append(funcionario)
                db.session.commit()
            return redirect(
                url_for("dashboard_alias", treinamento_id=turma.treinamento_id, turma_id=turma_id)
            )

        if action == "remove_funcionario":
            turma_id = request.form.get("turma_id", type=int)
            funcionario_id = request.form.get("funcionario_id", type=int)
            turma = db.session.get(Turma, turma_id)
            funcionario = db.session.get(Funcionario, funcionario_id)
            if turma and funcionario and funcionario in turma.funcionarios:
                turma.funcionarios.remove(funcionario)
                db.session.commit()
            return redirect(
                url_for("dashboard_alias", treinamento_id=turma.treinamento_id, turma_id=turma_id)
            )

        flash("Ação desconhecida.", "warning")
        return redirect(url_for("dashboard_alias"))

    treinamento_id = request.args.get("treinamento_id", type=int)
    turma_id = request.args.get("turma_id", type=int)

    treinamentos = Treinamento.query.order_by(Treinamento.titulo).all()
    treinamento_selecionado = db.session.get(Treinamento, treinamento_id) if treinamento_id else None
    turmas = treinamento_selecionado.turmas if treinamento_selecionado else []
    turma_selecionada = db.session.get(Turma, turma_id) if turma_id else None

    funcionarios_da_turma = []
    funcionarios_disponiveis = []
    if turma_selecionada:
        funcionarios_da_turma = turma_selecionada.funcionarios
        if not turma_selecionada.lotada and not turma_selecionada.encerrada:
            ids_vinculados = {f.id for f in funcionarios_da_turma}
            funcionarios_disponiveis = Funcionario.query.filter(
                Funcionario.ativo == True,
                ~Funcionario.id.in_(ids_vinculados),
            ).all()

    return render_template(
        "dashboard/dashboard.html",
        treinamentos=treinamentos,
        treinamento_selecionado=treinamento_selecionado,
        turmas=turmas,
        turma_selecionada=turma_selecionada,
        funcionarios_da_turma=funcionarios_da_turma,
        funcionarios_disponiveis=funcionarios_disponiveis,
        turma_lotada=turma_selecionada.lotada if turma_selecionada else False,
        turma_encerrada=turma_selecionada.encerrada if turma_selecionada else False,
    )


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
    app.run(host="0.0.0.0", port=5001, debug=True)
