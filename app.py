from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# Dados estáticos (lista de usuários)
lista = [
    {"id": 1, "nome": "Hudson", "senha": "hudson1234"},
    {"id": 2, "nome": "Maria", "senha": "maria1234"}
]

@app.get("/")
async def root():
    """Página inicial - redireciona para login"""
    return RedirectResponse(url="/login")

@app.get("/login")
async def get_login():
    """Mostra o formulário de login"""
    return HTMLResponse(content=open("login.html").read(), status_code=200)

@app.post("/login")
async def post_login(username: str = Form(...), password: str = Form(...)):
    """Processa o login (POST do formulário)"""
    for usuario in lista:
        if usuario["nome"] == username and usuario["senha"] == password:
            return HTMLResponse(content=open("home.html").read(), status_code=200)
    return HTMLResponse(content=open("login.html").read(), status_code=401)

@app.get("/home")
async def home():
    """Página home (após login)"""
    return HTMLResponse(content=open("home.html").read(), status_code=200)


