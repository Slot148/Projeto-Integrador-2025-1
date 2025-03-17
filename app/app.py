from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/atestado")
def ateestado():
    return render_template("atestados.html")

@app.route("/professor")
def professor():
    return render_template("professor.html")

@app.route("/scrum")
def scrum():
    return render_template("scrum.html")

@app.route("/scrum/registro")
def scrum_registro():
    return render_template("scrumregistro.html")