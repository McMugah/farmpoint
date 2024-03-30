from flask import render_template, redirect, url_for, flash, request
from ..models import  Product
from ..forms.form import ProductForm,CartItemForm
from app import db
from . import api


# Product Routes
@api.route('/create_product', methods=['GET', 'POST'])
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            quantity=form.quantity.data
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('api.products_list'))
    return render_template('create_product.html', form=form)


@api.route('/products')
def products_list():
    products = Product.query.all()
    form = CartItemForm()
    return render_template('product_list.html', products=products, form=form)


@api.route('/update_product/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('api.products_list'))
    return render_template('update_product.html', form=form, product=product)


@api.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('api.products_list'))


@api.route('/product/<int:product_id>')
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)
