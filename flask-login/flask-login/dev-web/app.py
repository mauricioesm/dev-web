from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user, login_user
from pathlib import Path
import secrets
from extensions import db, login_manager, mail
from flask_mail import Message
from config import Config
from extensions import db, login_manager
from models.usuario_models import Usuario

app = Flask(__name__)

# Garante que a pasta instance exista
Path(app.instance_path).mkdir(parents=True, exist_ok=True)

# Configurações
app.config.from_object(Config)
app.config["APP_RUN_ID"] = secrets.token_hex(16)

# Inicializa extensões
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = None


# Rota de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    user = Usuario.query.filter_by(email=email).first()

    if user and user.check_password(password):
        login_user(user)
        session["app_run_id"] = app.config["APP_RUN_ID"]
        return redirect(url_for("home"))

    flash("Email ou senha inválidos")
    return redirect(url_for("login"))


# Rota principal
@app.route("/")
@login_required
def home():
    first_name = current_user.nome.split()[0] if current_user.nome else "Usuario"
    return render_template("auth/login.html", user=first_name)


# Executar aplicação
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


# Flask-Login: carregar usuário
@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(Usuario, int(user_id))
    except (TypeError, ValueError):
        return None


# Expirar sessão quando reiniciar o app
@app.before_request
def expire_session_after_restart():
    if not current_user.is_authenticated:
        return None

    if session.get("app_run_id") != app.config["APP_RUN_ID"]:
        session.clear()


# Criar banco e usuário admin
with app.app_context():
    db.create_all()

    if not Usuario.query.filter_by(email="admin@seloedu.com").first():
        master = Usuario(
            nome="Admin Master",
            email="admin@seloedu.com",
            funcao="master"
        )
        master.set_password("123456")

        db.session.add(master)
        db.session.commit()


        from extensions import db, login_manager, mail

mail.init_app(app)
from itsdangerous import URLSafeTimedSerializer

def generate_reset_token(user_email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(user_email, salt="reset-password")


def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token, salt="reset-password", max_age=expiration)
    except:
        return None
    return email

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        return render_template("auth/forgot_password.html")

    email = request.form.get("email")
    user = Usuario.query.filter_by(email=email).first()

    if user:
        token = generate_reset_token(user.email)

        reset_link = url_for("reset_password", token=token, _external=True)

        msg = Message("Redefinir senha", recipients=[user.email])
        msg.body = f"Acesse o link para redefinir sua senha: {reset_link}"

        mail.send(msg)

    flash("Se o email existir, você receberá instruções.")
    return redirect(url_for("login"))

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    email = verify_reset_token(token)

    if not email:
        flash("Token inválido ou expirado")
        return redirect(url_for("login"))

    user = Usuario.query.filter_by(email=email).first()

    if request.method == "GET":
        return render_template("auth/reset_password.html")

    password = request.form.get("password")

    user.set_password(password)
    db.session.commit()

    flash("Senha atualizada com sucesso")
    return redirect(url_for("login"))