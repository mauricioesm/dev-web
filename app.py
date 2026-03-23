from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

logins = {
    "Jhonatas": "1206",
    "Adriano": "1304",
    "Victory": "1608"
}

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in logins and logins[username] == password:
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="erro no login")
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)