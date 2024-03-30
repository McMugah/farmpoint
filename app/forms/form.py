from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DecimalField, IntegerField,BooleanField,FloatField,HiddenField,SelectField, DateField,RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange,InputRequired


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Description')
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Product')


class OrderForm(FlaskForm):
    status_choices = [('Pending', 'Pending'), ('Processing', 'Processing'), ('Completed', 'Completed')]
    status = SelectField('Status', choices=status_choices, validators=[DataRequired()])
    submit = SubmitField('Update Status')

class OrderConfirmationForm(FlaskForm):
    confirm_order = SubmitField('Confirm Order')


class OrderItemForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Add to Order')


class CartItemForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[InputRequired(), NumberRange(min=1)])
    submit = SubmitField('Add/Update Item')


# Updatating Cart
class UpdateQuantityForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[InputRequired(), NumberRange(min=1)])
    submit = SubmitField('Update Quantity')

class RemoveItemForm(FlaskForm):
    submit = SubmitField('Remove Item')


class CheckoutForm(FlaskForm):
    shipping_address = StringField('Shipping Address', validators=[DataRequired()])
    payment_method = SelectField('Payment Method', validators=[DataRequired()])
    credit_card_number = StringField('Credit Card Number', validators=[DataRequired(), Length(min=16, max=16, message='Credit card number must be 16 digits long')])
    expiration_date = StringField('Expiration Date', validators=[DataRequired(), Length(min=5, max=5, message='Invalid expiration date format')])
    cvv = StringField('CVV', validators=[DataRequired(), Length(min=3, max=3, message='CVV must be 3 digits long')])
    submit = SubmitField('Proceed to Payment')


    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        payment_methods = kwargs.get('payment_methods', [])
        self.payment_method.choices = [(method, method.capitalize()) for method in payment_methods]

