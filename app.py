from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

usuarios_login = [
    {"username": "Aluno1", "password": "123"},
    {"username": "Aluno2", "password": "123"},
    {"username": "Aluno3", "password": "123"}
]

@app.get("/login")
def fazer_login(username: str = None, password: str = None):
    if username is None or password is None:
        return FileResponse("login.html")
    for usuario in usuarios_login:
        if usuario["username"] == username and usuario["password"] == password:
            return RedirectResponse(url="/home")

@app.get("/home")
def abrir_home():
    return FileResponse("home.html")

# @app.get("/login")
# def fazer_login(username: str = None, password: str = None):
#     if username is None or password is None:
#         return FileResponse("login.html")
#     for usuario in usuarios_login:
#         if usuario["username"] == username and usuario["password"] == password:
#             return RedirectResponse(url="/home.html")

# @app.get("/home")
# def abrir_home():
#     return FileResponse("home.html")