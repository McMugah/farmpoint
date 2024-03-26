import jwt
from datetime import datetime,timedelta

from . import db, login_manager,bcrypt
from flask_login import UserMixin
from flask import current_app
from werkzeug.security import check_password_hash,generate_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    user_type = db.Column(db.String(50))

    # Added to differentiate user types
    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self, expiration=3600):
        payload = {
            "id": self.id,
            "exp": datetime.utcnow() + timedelta(seconds=expiration),
        }
        token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
        return token


    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            return payload["id"]
        except jwt.exceptions.ExpiredSignatureError:
            return None  # Handle expired token error
        except jwt.exceptions.InvalidTokenError:
            return None  # Handle invalid token error

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


class Farmer(User):
    __tablename__ = 'farmers'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    farm_name = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', backref='farmer', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'farmer',
    }

class Customer(User):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'