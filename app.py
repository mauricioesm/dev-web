import secrets

from flask import Flask,render_template, request, redirect, url_for, abort, session
from flask_login import login_required, current_user, logout_user, login_user
from flask_mail import Mail, Message
from extensions import login_manager, db
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from models.usuarios_models import Usuario
from config import Config
import os

app = Flask(__name__, static_folder='static', template_folder='static') 
app.config.from_object(Config)
app.config["APP_RUN_ID"] = secrets.token_hex(16)

db.init_app(app)
login_manager.init_app(app)
"""
login_manager.login_view = "login"
login_manager.login_message = None
"""

# Configuração do MailHog
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None
app.config['MAIL_DEFAULT_SENDER'] = 'suporte@suaapp.com'

mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(Usuario, int(user_id))
    except Exception as e:
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

with app.app_context():
    db.create_all()
    if not Usuario.query.filter_by(email="admin@seloedu.com").first():
        master = Usuario(
            name = "Admin Master",
            email = "admin@seloedu.com",
            funcao = "master",
        )

        master.set_password("123456")
        db.session.add(master)
        db.session.commit()

def validate_on_subtmit():
    email = db.session.get("email")
    usuario = db.session.get("usuario")
    if email is None:
        return False
    
    if usuario is None:
        return False

    return True


def gerar_token(email):
    return salt.dumps(email, salt="recuperar-senha")

def validar_token(token, validade=3600):
    try:
        email = salt.loads(token, salt="recuperar-senha", max_age=validade)
        return email
    except Exception as e:
        return None

@app.route('/')
@login_required
def home():
    first_name = (current_user.name or "Usuario").split()[0]
    return render_template('home.html', user=first_name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Usuario.query.filter_by(name=username).first()

        if user and check_password_hash(user.senha_hash, password):
            login_user(user)
            session["app_run_id"] = app.config["APP_RUN_ID"]
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/send_test_email')
def send_test_email():
    msg = Message("Teste de Email", recipients=["usuario-teste@gmail.com"])
    msg.body = "Este é um email de teste enviado pelo Flask-Mail usando o MailHog."
    mail.send(msg)
    return "Email de teste enviado! MailHog em http://localhost:8025"

salt = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@app.route('/redefinir-senha', methods=['GET','POST'])
def esqueci_senha():
    if request.method == 'POST':
        name_identificado = request.form.get('username')

        user = Usuario.query.filter_by(name=name_identificado).first()

        if user and user.email:
            token = gerar_token(user.email)
            link = url_for('redefinir_senha', token=token, _external=True)

            msg = Message("Redefinição de Senha", recipients=[user.email])
            msg.body = f"Olá {user.name},\n\nClique no link abaixo para redefinir sua senha:\n{link}\n"
            mail.send(msg)

    return """
        <form method="post">
            <p>Digite seu nome de usuário para recuperar a senha:</p>
            <input name="username" placeholder="Username" required>
            <button type="submit">Enviar E-mail</button>
        </form>"""

@app.route('/redefinir-senha/<token>', methods=['GET','POST'])
def redefinir_senha(token):

    email_adquirido = validar_token(token)

    if not email_adquirido:
        return "Link já expirou"
    

    if request.method == 'POST':
        nova_senha = request.form.get('password')
        confirmacao = request.form.get('confirm_password')

        if nova_senha != confirmacao:
            return "Senhas diferentes", 400
        
        user = Usuario.query.filter_by(email=email_adquirido).first()

        if user:
            user.senha_hash = generate_password_hash(nova_senha)
            db.session.commit()
            return "Senha redefinida com sucesso! Você já pode fazer login com a nova senha."
        
        return "Usuário não encontrado", 404  

    return """
        <form method="post">
            <input name="password" type="password" placeholder="Nova Senha" required>
            <input name="confirm_password" type="password" placeholder="Confirme a Senha" required>
            <button type="submit">Alterar Senha</button>
        </form>
           """

if __name__ == '__main__':
    app.run(debug=True, port=5000)