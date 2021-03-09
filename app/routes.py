#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""HTTP route definitions"""

from flask import request, render_template
from app import app
from app.database import create, read, update, delete, scan
from datetime import datetime
from app.forms.product import ProductForm
import sqlite3

DATABASE="catalog_db"

def get_db():
    db = getattr(g, "_database", None)
    if not db:
        db = g._database = sqlite3.connect(DATABASE)
    return db




@app.route('/')
def index():
    return render_template("index.html")


@app.route("/product_form", methods=["GET", "POST"])
def product_form():
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        category = request.form.get("category")
        description = request.form.get("description")
        quantity = request.form.get("quantity")
        create(name, price, category, description, quantity)
    form = ProductForm()
    return render_template("form_example.html", form=form)


@app.route("/products")
def get_all_products():
    out = scan()
    # out["ok"] = True
    # out["message"] = "Success"
    # return out
    return render_template("products.html", products=out["body"])


# @app.route("/products/<pid>")
# def get_one_product(pid):
#     out = read(int(pid))
#     out["ok"] = True
#     out["message"] = "Success"
#     return out


@app.route("/products", methods=["POST"])
def create_product():
    product_data = request.json
    new_id = create(
        product_data.get("name"),
        product_data.get("price"),
        product_data.get("category"),
        product_data.get("description"),
        product_data.get("quantity") 
    )

    return {"ok": True, "message": "Success", "new_id": new_id}



@app.route("/products/<pid>", methods=["GET", "PUT"])
def update_product(pid):
    # product_data = request.json
    if request.method == "PUT":
        update(pid, request.form)
        return {"ok": "True", "message": "Updated"}
    out = read(int(pid))
    update_form = ProductForm()
    if out["body"]:
        return render_template("single_product.html", product=out["body"][0], form=update_form)
    else:
        return render_template("404.html"), 404
    

@app.route("/products/delete/<pid>", methods=["GET"])
def delete_product(pid):
    new_pid = int(pid)
    out = delete(new_pid)
    return render_template("delete.html")


@app.route("/user/<name>")
def show_user(name):
    return render_template("user.html", name=name)



@app.route('/agent')
def agent():
    user_agent = request.headers.get("User-Agent")
    return "<p>Your user agent is %s</p>" % user_agent


@app.route('/myroute')
def my_view_function():
    return render_template("index.html")


@app.route("/about_me")
def about_me():
    return render_template("about_me.html", first_name="Miguel", last_name="Rodriguez", hobbies="Mountain biking")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404





# CAN'T SEEM TO FIND THE BEST WAY TO CONNECT TO THE REVIEW DATABASE


# @app.route('/submit', methods=['POST'])
# def submit():
#     if request.method == "POST":
#         id = request.form.get("id")
#         prod_id = request.form.get("prod_id")
#         review = request.form.get("review")
#         if id == '':
#             return render_template('single_production.html', message='Please enter required field')
#         return render_template("submit.html")


# class FeedBack(db.Model):
#     __tablename__ = 'feedback'
#     id = db.Column(db.Integer, primary_key=TRUE)
#     prod_id = db.Column(db.Integer)
#     review = db.Column(db.Text())

#     def __init__(self, prod_id, review):
#         self.prod_id = prod_id
#         self.review = review



if __name__ == '__main__':
    app.debug = True
    app.run()