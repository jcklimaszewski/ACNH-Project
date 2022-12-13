from flask import render_template, session, redirect, flash
from flask_app import app
import requests
import json

@app.route("/fish/home", methods=["GET"])
def fish_index():
    if "user_id" not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect("/")

    req = requests.get("https://acnhapi.com/v1/fish")
    data = json.loads(req.content)
    print(data['bitterling']['id'])
    return render_template("home_fish.html", data_names=data)

@app.route("/insects/home", methods=["GET"])
def bug_index():
    if "user_id" not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect("/")

    req = requests.get("https://acnhapi.com/v1/bugs")
    data = json.loads(req.content)
    print(data)
    return render_template("home_insects.html", data_names=data)