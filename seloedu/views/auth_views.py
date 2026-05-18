from flask import current_app, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user, logout_user
from flask_mail import Message

from extensions import db, mail
from models.usuario_models import Usuario
from utils.token_utils import confirm_token, generate_token


def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard_alias"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = Usuario.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            session["app_run_id"] = current_app.config.get("APP_RUN_ID")
            return redirect(url_for("dashboard_alias"))

        return render_template("auth/login.html", email=email, error="E-mail ou senha invalido."), 401

    return render_template("auth/login.html", email="")


def logout():
    logout_user()
    session.clear()
    return redirect(url_for("auth.login"))


def forgot_password():
    message = None
    message_category = None
    reset_url = None

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = Usuario.query.filter_by(email=email).first()

        if user:
            token = generate_token(user.email)
            reset_url = url_for("auth.reset_password", token=token, _external=True)
            msg = Message(
                subject="Redefinicao de senha - SELOEDU",
                recipients=[user.email],
                body=f"Use o link para redefinir sua senha: {reset_url}",
            )
            try:
                mail.send(msg)
                message = "Enviamos o link de redefinicao para o e-mail informado."
                message_category = "success"
            except Exception:
                # Fallback para ambiente local sem SMTP ativo.
                message = "MailHog indisponivel. Use o link de teste abaixo para redefinir a senha."
                message_category = "danger"
        else:
            message = "Nao encontramos esse e-mail."
            message_category = "danger"

    return render_template(
        "auth/forgot_password.html",
        message=message,
        message_category=message_category,
        reset_url=reset_url,
    )


def reset_password():
    token = request.values.get("token", "").strip()
    message = None
    message_category = None

    if not token:
        message = "Token ausente para redefinicao."
        message_category = "danger"
        return render_template(
            "auth/reset_password.html",
            token="",
            message=message,
            message_category=message_category,
        ), 400

    email = confirm_token(token)
    if not email:
        message = "Token invalido ou expirado."
        message_category = "danger"
        return render_template(
            "auth/reset_password.html",
            token="",
            message=message,
            message_category=message_category,
        ), 400

    user = Usuario.query.filter_by(email=email).first()
    if user is None:
        message = "Usuario nao encontrado para redefinicao."
        message_category = "danger"
        return render_template(
            "auth/reset_password.html",
            token="",
            message=message,
            message_category=message_category,
        ), 404

    if request.method == "POST":
        password = request.form.get("password", "")
        if not password:
            message = "Informe uma nova senha."
            message_category = "danger"
            return render_template(
                "auth/reset_password.html",
                token=token,
                message=message,
                message_category=message_category,
            ), 400

        user.set_password(password)
        db.session.commit()
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", token=token)


class AuthViews:
    login = staticmethod(login)
    logout = staticmethod(logout)
    forgot_password = staticmethod(forgot_password)
    reset_password = staticmethod(reset_password)


auth = AuthViews
