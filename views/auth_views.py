from extensions import login_manager, mail
from flask import render_template, request, redirect, url_for, session, current_app
from flask_login import login_user
from flask_mail import Message
from models.usuarios_models import Usuario, db
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash


def login():
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Usuario.query.filter_by(name=username).first()

        if user and check_password_hash(user.senha_hash, password):
            login_user(user)
            session["app_run_id"] = current_app.config.get("APP_RUN_ID")
            return redirect(url_for('home'))

    return render_template('login.html')


def send_test_email():
    msg = Message("Teste de Email", recipients=["usuario-teste@gmail.com"])
    msg.body = "Este é um email de teste enviado pelo Flask-Mail usando o MailHog."
    mail.send(msg)
    return "Email de teste enviado! MailHog em http://localhost:8025"

def esqueci_senha():
    if request.method == 'POST':
        name_identificado = request.form.get('username')

        user = Usuario.query.filter_by(name=name_identificado).first()

        if user and user.email:
            token = gerar_token(user.email)
            link = url_for('auth_login.redefinir_senha', token=token, _external=True)

            msg = Message("Redefinição de Senha", recipients=[user.email])
            msg.body = f"Olá {user.name},\n\nClique no link abaixo para redefinir sua senha:\n{link}\n"
            mail.send(msg)

            return redirect(url_for("auth_login.login"))

    return render_template('reset_password.html')


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

    return render_template('login.html')

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(Usuario, int(user_id))
    except Exception as e:
        return None
    

def validate_on_subtmit():
    email = db.session.get("email")
    usuario = db.session.get("usuario")
    if email is None:
        return False
    
    if usuario is None:
        return False

    return True

def gerar_token(email):
    salt = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))

    return salt.dumps(email, salt="recuperar-senha")

def validar_token(token, validade=3600):
    salt = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))

    try:
        email = salt.loads(token, salt="recuperar-senha", max_age=validade)
        return email
    except Exception as e:
        return None