from flask import render_template
from . import api


@api.route("/")
def get_homepage():
    return render_template("home.html")
