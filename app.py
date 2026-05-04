import secrets
from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from config import Config
from extensions import db, login_manager
from models.usuario_models import Usuario
from routes.auth_rotas import auth_bp;


app = Flask(__name__)
app.register_blueprint(auth_bp)

Path(app.instance_path).mkdir(parents=True, exist_ok=True)
app.config.from_object(Config)
app.config["APP_RUN_ID"] = secrets.token_hex(16)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.login_message = None

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Criar usuário de teste se não existir
        if not Usuario.query.filter_by(email='admin@seloedu.com').first():
            admin = Usuario(
                nome='Administrador',
                email='admin@seloedu.com',
                funcao='coordenador'
            )
            admin.set_password('123')
            db.session.add(admin)
            db.session.commit()
            print("Usuário de teste criado: admin@seloedu.com / 123")
    app.run(debug=True)

