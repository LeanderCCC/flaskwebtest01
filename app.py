from flask import Flask, render_template, redirect, request, session
from flask_session import Session
 
app = Flask(__name__)
app.secret_key = "b_5#y2L'F4Q8z\n\xec]/"

@app.route("/", methods=["GET", "POST"])
def hello_world():
    
    if request.method == "POST":
        session["name"] = request.form['name']
        return render_template("index.html", name=session["name"])
    
    else:
        return render_template("index.html")
    
# (session["id"] == "" and session["password"] == "")

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        if session["name"] == "" or request.form['name'] == "":
            return render_template("login.html")
        else:
            session["name"] = request.form['name']
            return redirect("/")

@app.route("/logout", methods=["POST"])
def logout():
    if request.method == "POST":
        session["name"] = ""
        return redirect("/")