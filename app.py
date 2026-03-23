from flask import Flask
from flask import render_template

app = Flask(__name__)

# app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return render_template("login.html")

@app.get("/login")
def login():
    return render_template("login.html")

@app.post("/login")
def login_post():
    return render_template("home.html", status_code= 303)

@app.get("/home")
def home():
    return render_template("home.html")
