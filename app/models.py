from . import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash,generate_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    user_type = db.Column(db.String(50))  # Added to differentiate user types

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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