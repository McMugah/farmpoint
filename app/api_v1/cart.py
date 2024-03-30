from flask import render_template, redirect, url_for, flash, request
from datetime import datetime
from flask_login import current_user,login_required
from ..models import  Cart, CartItem, Product, Order,OrderItem
from ..forms.form import UpdateQuantityForm, ProductForm,CartItemForm,RemoveItemForm,CheckoutForm,OrderForm,OrderItemForm,OrderConfirmationForm
from app import db
from . import api






# Cart Routes
@api.route('/view_cart')
@login_required
def view_cart():
    cart = current_user.cart
    total_amount = 0
    for item in cart.items:
        if item.product.price is not None and item.quantity is not None:
            total_amount += item.product.price * item.quantity
    return render_template('view_cart.html', cart=cart, total_amount=total_amount, user=current_user)


@api.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    form = CartItemForm()
    if form.validate_on_submit():
        quantity = form.quantity.data
        product = Product.query.get(product_id)
        if product:
            cart = current_user.cart
            if cart is None:
                cart = Cart(user_id=current_user.id)
                db.session.add(cart)
                db.session.commit()
            cart_id = cart.id
            cart_item = CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first()
            if cart_item:
                cart_item.quantity += quantity
            else:
                cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
                db.session.add(cart_item)
            db.session.commit()
            flash('Item added to cart successfully.', 'success')
            return redirect(url_for('api.view_cart'))
        else:
            flash('Invalid product ID.', 'danger')
    return redirect(url_for('api.view_cart'))


@api.route('/remove_from_cart/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    form = RemoveItemForm()
    if form.validate_on_submit():
        cart_item = CartItem.query.get_or_404(cart_item_id)
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart successfully.', 'success')
    return redirect(url_for('api.view_cart'))



@api.route('/update_cart_item/<int:cart_item_id>', methods=['POST'])
@login_required
def update_cart_item(cart_item_id):
    form = UpdateQuantityForm()
    if form.validate_on_submit():
        cart_item = CartItem.query.get_or_404(cart_item_id)
        cart_item.quantity = form.quantity.data
        db.session.commit()
        flash('Quantity updated successfully.', 'success')
    return redirect(url_for('api.view_cart'))



@api.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    available_payment_methods = ['credit_card', 'mpesa']
    form = CheckoutForm(payment_methods=available_payment_methods)
    if form.validate_on_submit():
        total_amount = 0
        for item in current_user.cart.items:
            if item.product.price is not None and item.quantity is not None:
                total_amount += item.product.price * item.quantity
        if current_user.cart.items:
            order = Order(user_id=current_user.id, total_amount=total_amount)
            db.session.add(order)
            for cart_item in current_user.cart.items:
                order_item = OrderItem(order=order, product=cart_item.product, quantity=cart_item.quantity)
                db.session.add(order_item)
            current_user.cart.items.clear()
            db.session.commit()
            flash('Order placed successfully!', 'success')
            return redirect(url_for('api.order_confirmation'))
        else:
            flash('Your cart is empty. Please add items before checking out.', 'warning')
    return render_template('checkout.html', form=form)



@api.route('/view_cart/checkout', methods=['GET', 'POST'])
@login_required
def checkout_from_cart():
    available_payment_methods = ['credit_card', 'mpesa']
    form = CheckoutForm(payment_methods=available_payment_methods)
    if form.validate_on_submit():
        total_amount = sum(item.product.price * item.quantity for item in current_user.cart.items
                           if item.product.price is not None and item.quantity is not None)
        if current_user.cart.items:
            order = Order(user_id=current_user.id, total_amount=total_amount)
            db.session.add(order)
            db.session.commit()
            for cart_item in current_user.cart.items:
                if cart_item.cart_id is None:
                    flash('Error: Cart ID is missing for cart item.', 'danger')
                    return redirect(url_for('api.view_cart'))
                order_item = OrderItem(order=order, product=cart_item.product, quantity=cart_item.quantity)
                db.session.add(order_item)
            current_user.cart.items.clear()
            db.session.commit()
            flash('Order placed successfully!', 'success')
            return redirect(url_for('api.order_confirmation'))
        else:
            flash('Your cart is empty. Please add items before checking out.', 'warning')
    return render_template('checkout.html', form=form)

# Order Routes
@api.route('/create_order', methods=['GET', 'POST'])
def create_order():
    order_form = OrderForm()
    order_item_form = OrderItemForm()
    if order_form.validate_on_submit() and order_item_form.validate_on_submit():
        order = Order(status=order_form.status.data)
        order.save()
        product_id = request.form.get('product_id')
        product = Product.query.get(product_id)
        quantity = order_item_form.quantity.data
        order_item = OrderItem(product=product, quantity=quantity)
        order_item.save()
        product.quantity -= quantity
        product.save()
        return redirect(url_for('api.order_success'))
    return render_template('create_order.html', order_form=order_form, order_item_form=order_item_form)


@api.route('/order_success')
def order_success():
    return render_template('order_success.html')


@api.route('/confirm_order', methods=['POST'])
def confirm_order():
    confirmation_form = OrderConfirmationForm()
    if confirmation_form.validate_on_submit():
        order_id = request.form.get('order_id')
        order = Order.query.get(order_id)
        order.status = 'Confirmed'
        order.save()
        return redirect(url_for('api.order_success'))
    return redirect(url_for('api.create_order'))


@api.route('/process_order', methods=['POST'])
@login_required
def process_order():
    order_form = OrderForm()
    if order_form.validate_on_submit():
        new_status = order_form.status.data
        flash(f'Order status updated to {new_status} successfully!', 'success')
        return redirect(url_for('api.products_list'))
    return redirect(url_for('api.create_order'))






















# #checkout Routes
# @api.route('/checkout', methods=['POST'])
# @login_required
# def checkout():
#     cart = current_user.cart
#     form = PaymentForm()
#     if form.validate_on_submit():
#         phone_number = form.phone_number.data
#         amount = form.amount.data
#         if cart.items:
#             order = Order.create_order(current_user.id, [item.product for item in cart.items])
#             checkout = Checkout(user_id=current_user.id, total_price=cart.calculate_total_cost())
#             db.session.add(checkout)
#             cart.items.clear()
#             db.session.commit()
#             flash('Checkout successful. Order created.', 'success')
#             return redirect(url_for('api.view_order', order_id=order.id))
#         else:
#             flash('Your cart is empty. Please add items before checkout.', 'danger')
#     return redirect(url_for('api.view_cart'))


# api.route('/checkout', methods=['GET', 'POST'])
# def checkout():
#     form = CheckoutForm()
#     if form.validate_on_submit():
#         shipping_address = form.shipping_address.data
#         contact_details = form.contact_details.data
#         selected_payment_method = form.payment_method.data
#         payment_successful = True
#         if payment_successful:
#             return render_template('order_success.html')
#         else:
#             return "Payment Failed! Please try again."
#     return render_template('checkout.html', form=form)
