from datetime import timedelta, datetime
from . import db, login_manager,bcrypt,jwt
from flask_login import UserMixin
from flask_jwt_extended import create_access_token



# Define the association table for the many-to-many relationship between orders and items
order_item = db.Table('order_item',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Establishing one-to-many relationship with orders
    orders = db.relationship('Order', backref='user', lazy=True)

    # One-to-one relationship with cart
    cart = db.relationship('Cart', uselist=False, back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_token(self, expiration=3600):
        token = create_access_token(identity=self.id, expires_delta=timedelta(seconds=expiration))
        return token

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Establishing many-to-many relationship with orders using association table
    orders = db.relationship('Order', secondary='order_product', backref='products_associated', lazy=True)

    def __repr__(self):
        return f'<Product {self.name}>'


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Establishing many-to-many relationship with products using association table
    products = db.relationship('Product', secondary='order_product', backref='orders_associated', lazy=True)

    def __repr__(self):
        return f'<Order {self.id}>'


# Association table for the many-to-many relationship between orders and products
order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)




class Item(db.Model):
    __tablename__="item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Establishing many-to-many relationship with orders using association table
    orders = db.relationship('Order', secondary=order_item, backref='items', lazy=True)

    def __repr__(self):
        return f'<Item {self.name}>'


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-one relationship with user
    user = db.relationship('User', back_populates='cart')

    # One-to-many relationship with cart items
    items = db.relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')


class CartItem(db.Model):
    __tablename__ = 'cart_item'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Many-to-one relationship with cart
    cart = db.relationship('Cart', back_populates='items')

    # Many-to-one relationship with product
    product = db.relationship('Product')



class Checkout(db.Model):
    __tablename__ = 'checkout'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
