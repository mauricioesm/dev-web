from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return FileResponse("login.html")

@app.get("/login")
def login():
    return FileResponse("login.html")

@app.post("/login")
def login_post():
    return RedirectResponse(url="/home", status_code= 303)

@app.get("/home")
def home():
    return FileResponse("home.html")
