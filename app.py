import secrets
from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from config import config
from extensions import db, login_manager
from models.usuario_models import Usuario
# from routes.auth_rotas import auth_bp;

# app.register_blueprint(auth_bp)

app = Flask(__name__)

Path(app.instance_path).mkdir(parents=True, exist_ok=True)
app.config.from_object(Config)
app.config["APP_RUN_ID"] = secrets.token_hex(16)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = None

# @login_manager.user_loader
# def load_user(user_id):
#     return Usuario.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

