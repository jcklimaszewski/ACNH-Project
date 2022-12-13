from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask import flash
from flask_app.models.user import User

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register_user", methods=["POST"])
def register():
    valid_user = User.create_user(request.form)

    if not valid_user:
        return redirect("/")
    
    session["user_id"] = valid_user.id
    
    return redirect("/fish/home")

@app.route("/login_user", methods=["POST"])
def login():
    valid_user = User.authenticate_user(request.form)
    if not valid_user:
        return redirect("/")

    session["user_id"] = valid_user.id
    return redirect("/fish/home")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")