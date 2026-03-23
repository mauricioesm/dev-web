from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# No Flask, por padrão, ele procura HTML na pasta 'templates' 
# e CSS/JS na pasta 'static'.

usuarios_login = [
    {"username": "Aluno1", "password": "123"},
    {"username": "Aluno2", "password": "123"},
    {"username": "Aluno3", "password": "123"}
]

@app.route("/login", methods=["GET"])
def fazer_login():
    # Pegando os parâmetros da URL (query strings)
    username = request.args.get("username")
    password = request.args.get("password")

    if username is None or password is None:
        # render_template busca o arquivo dentro da pasta 'templates'
        return render_template("login.html")
    
    for usuario in usuarios_login:
        if usuario["username"] == username and usuario["password"] == password:
            return redirect(url_for("abrir_home"))
    
    return render_template("login.html") # Se errar o login, volta para a página

@app.route("/home")
def abrir_home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)