from flask import render_template, redirect, url_for, flash, request,jsonify
from urllib.parse import urlparse

from flask_login import login_user, current_user, logout_user, login_required
from ..models import  Product,Category
from ..forms.form import ProductForm,CartForm, CategoryForm
from app import db
from . import api

@api.route('/products/create', methods=['GET', 'POST'])
def create_product():
    form = ProductForm()
    category_form = CategoryForm()  # Create an instance of the CategoryForm
    form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]

    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            category_id=form.category_id.data
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('api.get_all_products'))
    return render_template('create_product.html', form=form, category_form=category_form)

# @api.route('/products', methods=['GET'])
# def get_all_products():
#     products = Product.query.all()
#     product_list = []
#     for product in products:
#         product_data = {
#             'id': product.id,
#             'name': product.name,
#             'price': product.price,
#             'description': product.description,
#             'category': product.category  # Assuming you have a 'category' attribute in your Product model
#         }
#         product_list.append(product_data)
#     form = CartForm()  # Create an instance of the CartForm
#     return render_template('products.html', products=product_list, form=form)

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
            'category': product.category.name if product.category else None,  # Access category name through the relationship
            'category_id': product.category.id if product.category else None  # Access category ID through the relationship
        }
        product_list.append(product_data)
    form = CartForm()  # Create an instance of the CartForm
    return render_template('products.html', products=product_list, form=form)




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
