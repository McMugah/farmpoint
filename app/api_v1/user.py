from . import api

from flask import render_template, redirect, url_for, jsonify,request
from ..forms.user import RegistrationForm,LoginForm
from app import db
from app.models import User



@api.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    contact_number=form.contact_number.data,
                    address=form.address.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



# @api.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     form = RegistrationForm(data=data)
#     if form.validate():
#         user = User(username=form.username.data,
#                     email=form.email.data,
#                     contact_number=form.contact_number.data,
#                     address=form.address.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         return jsonify({'message': 'User registered successfully'}), 201
#     errors = form.errors
#     return jsonify({'errors': errors}), 400







@api.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)
