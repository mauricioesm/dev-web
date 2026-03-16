from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
static = Jinja2Templates(directory="static")

urls_permitidas = [
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=urls_permitidas,          
    allow_credentials=True,
    allow_methods=["*"],            
    allow_headers=["*"],    
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
def hello():
    return "Hello world"

@app.get("/home")
async def home(request):
    return static.TemplateResponse("home.html", {"request":request})

@app.post("/login")
def login(username:str=Form(...), password:str=Form(...)):
    
    if(username != "admin" and password != 123456):
        return HTMLResponse(status_code=404)
    
    return RedirectResponse(url="/static/home.html", status_code=200)

