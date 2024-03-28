from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Enter your username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=80)], render_kw={"placeholder": "Enter your password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')], render_kw={"placeholder": "Confirm your password"})
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter your password"})
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)], render_kw={"placeholder": "Enter product name"})
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.01)], render_kw={"placeholder": "Enter product price"})
    description = TextAreaField('Description', render_kw={"placeholder": "Enter product description"})
    category = StringField('Category', render_kw={"placeholder": "Enter product category"})
    submit = SubmitField('Submit')

class OrderForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()], render_kw={"placeholder": "Enter user ID"})
    product_id = IntegerField('Product ID', validators=[DataRequired()], render_kw={"placeholder": "Enter product ID"})
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)], render_kw={"placeholder": "Enter quantity"})
    total_price = FloatField('Total Price', validators=[DataRequired(), NumberRange(min=0.01)], render_kw={"placeholder": "Enter total price"})
    submit = SubmitField('Submit')

class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)], render_kw={"placeholder": "Enter item name"})
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.01)], render_kw={"placeholder": "Enter item price"})
    description = TextAreaField('Description', render_kw={"placeholder": "Enter item description"})
    submit = SubmitField('Submit')
