from flask import Flask
from flask import render_template
from flask import send_file
from flask import redirect
from flask import flash
from flask import url_for
from flask import request

app = Flask(__name__)
@app.route("/")
def hello_world():
    return "<p>Oi</p>"

usuarios_login = [
    {"username": "Aluno1", "password":"123"},
    {"username": "Aluno2", "password":"123"},
    {"username": "Aluno3", "password":"123"}
]

@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name = None):
    return render_template("hello.html", person = name)

from flask import request

@app.route("/login", methods=["GET", "POST"])
def fazer_login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    for usuario in usuarios_login:
        if usuario["username"] == username and usuario["password"] == password:
            return redirect("/home")

    flash("Usuário inválido", "erro")
    return redirect("/login")
        
@app.get("/home")
def abrir_home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)

