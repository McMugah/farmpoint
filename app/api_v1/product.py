from flask import render_template, redirect, url_for, flash, request,jsonify
from urllib.parse import urlparse

from flask_login import login_user, current_user, logout_user, login_required
from ..models import  Product
from ..forms.form import ProductForm
from app import db
from . import api



@api.route('/products/create', methods=['GET', 'POST'])
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            category=form.category.data
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('api.home'))
    return render_template('create_product.html', form=form)


@api.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category': product.category
        }
        product_list.append(product_data)
    return render_template('products.html', products=product_list)



@api.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('productById.html', product=product)



@api.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})
