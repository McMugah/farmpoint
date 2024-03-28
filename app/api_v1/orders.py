from flask import render_template, redirect, url_for, flash, request,jsonify
from urllib.parse import urlparse

from flask_login import login_user, current_user, logout_user, login_required
from ..models import  Order
from ..forms.form import OrderForm
from app import db
from . import api



@api.route('/orders', methods=['POST'])
def create_order():
    form = OrderForm(request.form)
    if form.validate():
        # Create a new order using form data
        order = Order(
            user_id=form.user_id.data,
            product_id=form.product_id.data,
            quantity=form.quantity.data,
            total_price=form.total_price.data
        )
        db.session.add(order)
        db.session.commit()
        return jsonify({'message': 'Order created successfully'}), 201
    else:
        # If form validation fails, return error messages
        errors = form.errors
        return jsonify({'errors': errors}), 400