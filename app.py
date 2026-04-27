from flask import Flask
from flask import render_template
app = Flask(__name__)  
@app.route("/")
def hello_World():
    return "<p>Hello, World!</p>"

@app.route("/index/")
@app.route("/index/<name>")
def index(name=None):
    return render_template("index.html", person=name)

if __name__ == "__main__":
    app.run(debug=True)


    