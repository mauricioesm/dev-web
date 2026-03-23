from flask import Flask,render_template, request, redirect, url_for, abort
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static', template_folder='static') 

urls = [
    "http://localhost:5500",
    "http://127.0.0.1:5000"
]

CORS(app, origins=urls)

@app.route('/')
def hello():
    return "Hello World"

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == "admin" and password == "123456":
            return redirect(url_for('home'))
        
        abort(404)

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)