# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User, Farmer, Product

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Enter your username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email address"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter your password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Re-enter your password"})
    contact_number = StringField('Contact Number', validators=[DataRequired()], render_kw={"placeholder": "Enter your contact number"})
    address = StringField('Address', validators=[DataRequired()], render_kw={"placeholder": "Enter your address"})
    user_type = SelectField('User Type', choices=[('customer', 'Customer'), ('farmer', 'Farmer')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Enter product name"})
    price = FloatField('Price', validators=[DataRequired()], render_kw={"placeholder": "Enter product price"})
    submit = SubmitField('Add Product')


class FarmerForm(FlaskForm):
    farm_name = StringField('Farm Name', validators=[DataRequired()], render_kw={"placeholder": "Enter farm name"})
    products = StringField('Products', validators=[DataRequired()], render_kw={"placeholder": "Enter products (comma-separated)"})
    submit = SubmitField('Create Farmer Account')
