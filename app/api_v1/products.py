from flask import render_template
from . import api


@api.route("/products", methods=["GET"])
def get_products():
    return render_template("products.html")
