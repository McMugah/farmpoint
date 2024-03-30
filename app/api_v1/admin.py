from flask import render_template, url_for, flash, redirect

from ..models import Product
from . import api

# @api.route('/admin')
# def admin ():
#     return render_template('admin.html')

@api.route('/admin')
def admin():
    # Assuming you have some logic here to fetch the product
    product = Product.query.first()  # Assuming you want the first product
    return render_template('admin.html', product=product)

# @api.route('/admin')
# def admin():
#     product = Product.query.first()  # Fetch the first product from the database
#     if product is None:
#         flash('No products found.', 'warning')
#         # Handle the case where no product exists, such as redirecting to another page or rendering an error message
#         return redirect(url_for('api.view_products'))  # Redirect to another route
#     else:
#         return render_template('admin.html', product=product)
