from flask import render_template, redirect, url_for, flash, request,jsonify,session
from urllib.parse import urlparse
from flask_login import current_user
from flask_login import login_user, current_user, logout_user, login_required
from ..models import  Cart, CartItem
from ..forms.form import CartForm, UpdateQuantityForm
from app import db
from . import api





@api.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    form = CartForm()
    if form.validate_on_submit():
        quantity = form.quantity.data
        product_id = form.product_id.data
        user_id = current_user.id if current_user.is_authenticated else None
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if not cart_item:
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)
        else:
            cart_item.quantity += quantity
        db.session.commit()
        flash('Product added to cart successfully', 'success')
        return redirect(url_for('cart'))
    return render_template('cart.html', form=form)


@api.route('/update_quantity/<int:item_id>', methods=['POST'])
def update_quantity(item_id):
    form = UpdateQuantityForm()
    if form.validate_on_submit():
        quantity = form.quantity.data
        cart = current_user.cart  # Assuming the user is logged in
        if cart:
            cart.update_quantity(item_id, quantity)
            flash('Quantity updated successfully.', 'success')
            return redirect(url_for('cart'))
    flash('Failed to update quantity.', 'danger')
    return redirect(url_for('cart'))



@api.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    cart = current_user.cart  # Assuming the user is logged in
    if cart:
        cart.remove_item(item_id)
        flash('Item removed from cart successfully.', 'success')
        return redirect(url_for('cart'))
    flash('Failed to remove item from cart.', 'danger')
    return redirect(url_for('cart'))


@api.route('/cart', methods=['GET'])
def cart():
    form = CartForm()  # Create an instance of the form
    user_id = current_user.id if current_user.is_authenticated else None
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart_items = {}  # Empty dictionary for an empty cart
    else:
        cart_items = {item.product_id: item.quantity for item in cart.items}
    return render_template('cart.html', form=form, cart_items=cart_items)
