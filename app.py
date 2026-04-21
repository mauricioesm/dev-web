import secrets

from flask import Flask,render_template, session, current_app
from flask_login import login_required, current_user, logout_user
from extensions import login_manager, db, mail, config
from models.usuarios_models import Usuario
from routes.auth_rotas import auth_login

app = Flask(__name__, static_folder='templates', template_folder='templates') 
app.register_blueprint(auth_login, url_prefix='/auth')
app.config.from_object("config.Config")
app.config["APP_RUN_ID"] = secrets.token_hex(16)

db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

@app.route('/')
@login_required
def home():
    first_name = (current_user.name or "Usuario").split()[0]
    return render_template('home.html', user=first_name)

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

@app.before_request
def expire_session_after_restart():
    if not current_user.is_authenticated:
        return None
    
    if session.get("app_run_id") == current_app.config.get("APP_RUN_ID"):
        return None
    
    logout_user()
    session.clear()
    return None


if __name__ == '__main__':
    app.run(debug=True, port=5000)