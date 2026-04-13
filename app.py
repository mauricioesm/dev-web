import secrets

from flask import Flask,render_template, request, redirect, url_for, abort, session
from flask_login import login_required, current_user, logout_user, login_user
from extensions import login_manager, db
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

        if user and password == "123456":
            login_user(user)
            session["app_run_id"] = app.config["APP_RUN_ID"]
            return redirect(url_for('home'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)