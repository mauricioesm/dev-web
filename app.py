from flask_login import *
from flask import *
from flask_mail import Mail, Message
from models.usuario_models import Usuario
from extensions import db, login_manager
import secrets
from config import Config
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# 2. Constrói os caminhos para static e templates
template_dir = os.path.join(basedir, 'templates') # No seu caso, você definiu ambos na pasta static
static_dir = os.path.join(basedir, 'static')

app = Flask(__name__, 
            static_folder=static_dir, 
            template_folder=template_dir)

# Path(app.instance_path).mkdir(parents=True, exist_ok=True)
app.config.from_object(Config)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" # Adicione para testar
app.config["APP_RUN_ID"] = secrets.token_hex(16)

# login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
mail = Mail(app)



@app.route("/")
@login_required
def home():
    first_name = (current_user.name or "Usuario").split()[0]
    return render_template("home.html", first_name=first_name)

@app.route("/login", methods=["GET", "POST"])  
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = Usuario.query.filter_by(name=username).first()
        
        if user and password == "123456":
            session["app_run_id"] = app.config["APP_RUN_ID"]
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user() # Finaliza a sessão do usuário no Flask-Login
    session.clear() # Limpa os dados da sessão (incluindo o seu app_run_id)
    flash("Você saiu da conta.", "info")
    return redirect(url_for("login"))

@app.route("/esqueceu-senha", methods=["GET", "POST"])
def esqueceu_senha():
    if request.method == "POST":
        email = request.form.get("email")
        user = Usuario.query.filter_by(email=email).first()
        if user:
            token = user.get_reset_token()
            db.session.commit()
            link = url_for("redefinir_senha", token=token, _external=True)
            msg = Message("Redefinir Senha", recipients=[email],
                         html=f"<a href='{link}'>Clique aqui para redefinir</a>")
            mail.send(msg)
            flash("Email enviado!", "success")
        else:
            flash("Email não encontrado", "warning")
        return redirect(url_for("login"))
    return render_template("esqueceu_senha.html")

@app.route("/redefinir-senha/<token>", methods=["GET", "POST"])
def redefinir_senha(token):
    user = Usuario.query.filter_by(reset_token=token).first()
    if not user or not user.verify_reset_token(token):
        flash("Link inválido ou expirado", "danger")
        return redirect(url_for("login"))
    
    if request.method == "POST":
        user.set_password(request.form.get("senha"))
        user.reset_token = None
        db.session.commit()
        flash("Senha redefinida!", "success")
        return redirect(url_for("login"))
    return render_template("redefinir_senha.html")

@login_manager.user_loader
def load_user(user_id):
    try:
        # CORREÇÃO: Deve ser session (singular), não sessions
        return db.session.get(Usuario, int(user_id))
    except (TypeError, ValueError):
        return None

@app.before_request
def expire_session_after_retart():
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
            funcao = "master"
        )
        master.set_password("123456")
        db.session.add(master)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
