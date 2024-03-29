from flask import render_template, redirect, url_for, flash, request
from urllib.parse import urlparse

from flask_login import login_user, current_user, logout_user, login_required
from ..models import User
from ..forms.form import RegistrationForm, LoginForm
from app import db
from . import api

@api.route('/')
def get_home():
    return render_template('base.html')


@api.route('/home')
def home():
    return render_template('home.html')


@api.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email address is already registered. Please use a different email.', 'danger')
            return redirect(url_for('api.register'))
        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        token = user.generate_token()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('api.login', token=token))
    return render_template('register.html', form=form)



@api.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            token = user.generate_token()
            next_page = request.args.get('next')
            # Check if next_page is not set or contains a full URL
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('api.get_all_products')  # Use 'api.home' as the endpoint
            flash('Login successful!', 'success')
            return redirect(next_page)
        flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@api.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('api.home'))


@api.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return render_template('users.html', users=users)


# @api.route('/profile')
# @login_required
# def profile():
#     user = User.query.get(current_user.id)
#     if user:
#         return render_template('profile.html', user=current_user)
#     else:
#         return "User not found", 404
