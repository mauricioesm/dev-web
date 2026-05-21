import secrets
from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, logout_user
from config import Config
from extensions import db, login_manager, mail
from models.usuario_models import Usuario

from routes.auth_rotas import auth_bp
from routes.usuarios_rotas import usuarios_bp
from models.treinamento_models import Funcionario, Treinamento, Turma
from routes.treinamento_rotas import treinamentos_bp
from datetime import datetime


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
    return redirect(url_for("dashboard_alias"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard_alias():
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "delete_turma":
            turma_id = request.form.get("turma_id")
            turma = db.session.get(Turma, turma_id)
            if turma:
                db.session.delete(turma)
                db.session.commit()
                flash("Turma excluída com sucesso.", "success")
            return redirect(url_for("dashboard_alias", treinamento_id=request.form.get("treinamento_id")))
            
        elif action == "create_turma":
            treinamento_id = request.form.get("treinamento_id")
            vagas = request.form.get("vagas", type=int)
            d_inicio = request.form.get("data_inicio")
            d_fim = request.form.get("data_fim")
            
            nova_turma = Turma(
                treinamento_id=treinamento_id,
                vagas=vagas,
                data_inicio=datetime.strptime(d_inicio, '%Y-%m-%d').date() if d_inicio else None,
                data_fim=datetime.strptime(d_fim, '%Y-%m-%d').date() if d_fim else None
            )
            db.session.add(nova_turma)
            db.session.commit()
            flash("Turma criada com sucesso!", "success")
            return redirect(url_for("dashboard_alias", treinamento_id=treinamento_id))

        elif action == "create_funcionario":
            nome = request.form.get("nome")
            email = request.form.get("email")
            novo_func = Funcionario(nome=nome, email=email)
            db.session.add(novo_func)
            db.session.commit()
            flash("Funcionário cadastrado no sistema!", "success")
            return redirect(url_for("dashboard_alias", treinamento_id=request.form.get("treinamento_id"), turma_id=request.form.get("turma_id")))

        elif action == "add_funcionario":
            turma_id = request.form.get("turma_id")
            funcionario_id = request.form.get("funcionario_id")
            turma = db.session.get(Turma, turma_id)
            func = db.session.get(Funcionario, funcionario_id)
            if turma and func:
                turma.funcionarios.append(func)
                db.session.commit()
            return redirect(url_for("dashboard_alias", treinamento_id=turma.treinamento_id, turma_id=turma.id))

        elif action == "remove_funcionario":
            turma_id = request.form.get("turma_id")
            funcionario_id = request.form.get("funcionario_id")
            turma = db.session.get(Turma, turma_id)
            func = db.session.get(Funcionario, funcionario_id)
            if turma and func and func in turma.funcionarios:
                turma.funcionarios.remove(func)
                db.session.commit()
            return redirect(url_for("dashboard_alias", treinamento_id=turma.treinamento_id, turma_id=turma.id))

        return redirect(url_for("dashboard_alias"))

    treinamento_id = request.args.get("treinamento_id", type=int)
    turma_id = request.args.get("turma_id", type=int)

    treinamentos = Treinamento.query.all()
    treinamento_selecionado = db.session.get(Treinamento, treinamento_id) if treinamento_id else None
    
    turmas = treinamento_selecionado.turmas if treinamento_selecionado else []
    turma_selecionada = db.session.get(Turma, turma_id) if turma_id else None

    funcionarios_da_turma = turma_selecionada.funcionarios if turma_selecionada else []
    
    if turma_selecionada:
        ids_na_turma = [f.id for f in funcionarios_da_turma]
        if ids_na_turma:
            funcionarios_disponiveis = Funcionario.query.filter(Funcionario.id.notin_(ids_na_turma)).all()
        else:
            funcionarios_disponiveis = Funcionario.query.all()
    else:
        funcionarios_disponiveis = []

    turma_lotada = turma_selecionada.matriculados >= turma_selecionada.vagas if turma_selecionada else False
    turma_encerrada = (turma_selecionada.data_fim < datetime.now().date()) if (turma_selecionada and turma_selecionada.data_fim) else False

    return render_template(
        "dashboard/dashboard.html",
        treinamentos=treinamentos,
        treinamento_selecionado=treinamento_selecionado,
        turmas=turmas,
        turma_selecionada=turma_selecionada,
        funcionarios_da_turma=funcionarios_da_turma,
        funcionarios_disponiveis=funcionarios_disponiveis,
        turma_lotada=turma_lotada,
        turma_encerrada=turma_encerrada,
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
    #app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)
