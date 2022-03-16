from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
 
app = Flask(__name__)
app.secret_key = "b_5#y2L'F4Q8z\n\xec]/"

db = mysql.connector.connect(
    host="hts-husum.de",#localhost
    user="d038888d",#root
    password="leander2022",#Cain110305
    database="d038888d"#users
)
cursor = db.cursor()


# Index
@app.route("/")
def main():
    try:
        if session['name'] != "" and session['password'] != "":
            username = session['name']
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
            rows = cursor.fetchall()
    
            if check_password_hash(rows[0][2], request.form['password']):
                session["id"] = rows[0][0]
                session["name"] = rows[0][1]
                session["password"] = rows[0][2]
                session["loggedIn"] = True
        else:
            session["loggedIn"] = False
    finally:
        return render_template("index.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form['name']
        try:
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
            rows = cursor.fetchall()
        
            if check_password_hash(rows[0][2], request.form['password']):
                session["id"] = rows[0][0]
                session["name"] = rows[0][1]
                session["password"] = rows[0][2]
                session["loggedIn"] = True
                return redirect("/")
            else:
                session["fehler"] = True
                return render_template("login.html")
            
        except:
            session["fehler"] = True
            return render_template("login.html")
        
    else:
        return render_template("login.html")
        
        
# Logout
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session["name"] = ""
    session["loggedIn"] = False
    return redirect("/")


# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["name"]
        password = generate_password_hash(request.form["password"])
        cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
        db.commit()
        
        cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
        rows = cursor.fetchall()
        session["id"] = rows[0][0]
        session["name"] = rows[0][1]
        session["loggedIn"] = True
        return render_template("index.html")
    else:
        return render_template("register.html")
    
