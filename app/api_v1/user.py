from flask import render_template, redirect, url_for, flash
from . import api
from app.models import User
from app.forms.user import RegistrationForm,LoginForm
from app import db
from ..auth import login_required,verify_password


@api.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Extract form data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        contact_number = form.contact_number.data
        address = form.address.data
        user_type = form.user_type.data

        # Check if the email is already in use
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already registered. Please use a different email.', 'error')
            return redirect(url_for('api.register'))

        # Create a new user
        new_user = User(username=username, email=email, contact_number=contact_number, address=address, user_type=user_type)
        new_user.set_password(password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        # Generate a token for the new user
        token =  generate_token(new_user)
        # Flash a success message
        flash('Registration successful. You can now log in.', 'success')
        # Redirect the user to the login page
        return redirect(url_for('api.login'))

    # Render the registration form template for GET requests
    return render_template('register.html', form=form)


@api.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if verify_password(email, password):
            user = User.query.filter_by(email=email).first()
            token = user.generate_token()
            return redirect(url_for('api.get_dashboard', token=token))
        flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)