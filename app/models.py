from datetime import timedelta, datetime
from . import db, login_manager,bcrypt
from flask_login import UserMixin
from app.execeptions import ValidationError


# Define the association table for the many-to-many relationship between orders and items
order_item = db.Table('order_item',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
)

# Association table for the many-to-many relationship between orders and products
order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    extend_existing=True  # Add this line if needed
)

# Continue with other model definitions...

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
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')


    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

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

    def calculate_subtotal(self):
        return sum(item.product.price * item.quantity for item in self.items)

    def calculate_total_cost(self):
        return self.calculate_subtotal()

    def update_quantity(self, item_id, quantity):
        cart_item = CartItem.query.filter_by(cart_id=self.id, product_id=item_id).first()
        if cart_item:
            cart_item.quantity = quantity
            db.session.commit()

    def remove_item(self, item_id):
        cart_item = CartItem.query.filter_by(cart_id=self.id, product_id=item_id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define the relationship with Category
    category = db.relationship('Category', backref=db.backref('products', lazy=True))

    # Establishing many-to-many relationship with orders using association table
    orders = db.relationship('Order', secondary=order_product, back_populates='products')

    def __repr__(self):
        return f'<Product {self.name}>'

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define the relationship with Product using back_populates for one of the relationships
    products = db.relationship('Product', secondary=order_product, back_populates='orders')

    def __repr__(self):
        return f'<Order {self.id}>'

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

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Category {self.name}>'
