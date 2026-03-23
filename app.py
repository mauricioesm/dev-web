from flask import Flask, render_template, request

Usuarios = [
    {'username': 'admin', 'password': '1234'},
    {'username': 'user', 'password': '5678'},
    {'username': 'silvio', 'password': '2006'}
]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in Usuarios:
            if user['username'] == username and user['password'] == password:
                return render_template('home.html')
        return render_template('login.html', error='Invalid credentials')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)