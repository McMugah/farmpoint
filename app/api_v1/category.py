from flask import render_template, redirect, url_for, flash, request,jsonify,session
from urllib.parse import urlparse
from flask_login import current_user
from flask_login import login_user, current_user, logout_user, login_required
from ..models import  Category
from ..forms.form import CategoryForm
from app import db
from . import api

@api.route('/categories/create', methods=['GET', 'POST'])
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully!', 'success')
        return redirect(url_for('api.get_all_categories'))  # Redirect to the route that displays all categories
    return render_template('create_category.html', form=form)



@api.route('/categories', methods=['GET'])
def get_all_categories():
    categories = Category.query.all()
    return render_template('all_categories.html', categories=categories)
