from flask import render_template, redirect, url_for, flash, request,jsonify
from urllib.parse import urlparse
from flask_login import current_user
from flask_login import login_user, current_user, logout_user, login_required
from ..models import  Order, Product
from ..forms.form import OrderForm
from app import db
from . import api



@api.route('/orders/create', methods=['GET', 'POST'])
def create_order():
    form = OrderForm()
    if form.validate_on_submit():
        # Get data from the form
        product_id = form.product_id.data
        quantity = form.quantity.data

        # Find the product by its ID
        product = Product.query.get(product_id)
        if product is None:
            flash('Product does not exist.', 'danger')
            return redirect(url_for('api.create_order'))

        # Create the order and add the product to it
        order = Order(user_id=current_user.id)  # Assuming you have user authentication set up
        order.products.append(product)

        # Commit the order to the database
        db.session.add(order)
        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('api.get_all_orders'))
    return render_template('order.html', form=form)



@api.route('/orders', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    return render_template('get_orders.html', orders=orders)
