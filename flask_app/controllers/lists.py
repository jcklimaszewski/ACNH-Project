from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask import flash
from flask_app.models.user import User
from flask_app.models.list import List

@app.route("/lists/new_list")
def new_list_page():
    if "user_id" not in session:
        flash("Please login before accessing your lists!")
        return redirect("/")

    return render_template("create_list.html")

@app.route("/lists/my_lists")
def show_lists():
    if "user_id" not in session:
        flash("Please login before accessing your lists!")
        return redirect("/")

    lists = List.get_all_by_id(session["user_id"])
    user = User.get_by_id(session["user_id"])
    return render_template("lists.html", all_lists=lists, user=user)

@app.route("/post_list", methods = ["POST"])
def create_list():
    valid_list = List.create_list(request.form)
    if valid_list:
        return redirect(f'/lists/my_lists')
    return redirect (f"/lists/new_list")

@app.route("/lists/edit/<int:list_id>")
def edit_list_page(list_id):
    lists = List.get_by_id(list_id)
    user_id = User.get_by_id(session["user_id"])
    print(f"Get list by id: {lists}")
    return render_template("edit_list.html", this_list=lists)

@app.route("/lists/<int:list_id>", methods=["POST"])
def edit_list(list_id):
    valid_list = List.update_list(request.form)
    print(f"Here is the list: {valid_list}")
    if not valid_list:
        return redirect(f"/lists/edit/{list_id}")
        
    return redirect(f"/lists/my_lists")

@app.route("/lists/delete/<int:list_id>")
def delete_by_id(list_id):
    if "user_id" not in session:
        flash("Please login before accessing your lists!")
        return redirect("/")
        
    List.delete_list(list_id)
    return redirect("/lists/my_lists")

