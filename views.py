# Holds all the routes for app.py as to not to clutter app.py
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

views = Blueprint(__name__, 'views')
address = "348"

# Defines the home page and passes variables to the pages within templates folder using render_template
@views.route("")
def home():
    return render_template("index.html", website_name = "GovGenie")

# Defines the results page and passes variables to the pages within templates folder using render_template
@views.route("/results")
def results():
    return render_template("results.html")

# # Defines the Congressional page and passes variables to the pages within templates folder using render_template
@views.route("/congress")
def congress():
    return render_template("congress.html")

@views.route("/test")
def test():
    return render_template("test.html")

#################
# We can access json data using the following:
# def get_json():
#     return jsonify({"key": "value", "key2": "value2"})


# @views.route("/data")
# def get_data():
#     data = request.json
#     return jsonify(data)
#################

@views.route("/go-to-home")
def go_to_home():
    return redirect(url_for("views.home")) 
