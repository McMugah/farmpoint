from datetime import datetime

from flask_login import UserMixin

from app.execeptions import ValidationError

from . import bcrypt, db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship("Order", backref="customer", lazy=True)
    cart = db.relationship(
        "Cart", uselist=False, back_populates="user", cascade="all, delete-orphan"
    )
    carts = db.relationship("Cart", backref="owner", overlaps="user")
    user_carts = db.relationship("Cart", backref="customer", overlaps="user")

    def __repr__(self):
        return f"<User id={self.id}, username={self.username}>"

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False)  # Quantity in stock
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    order_items = db.relationship("OrderItem", back_populates="product")
    cart_items = db.relationship("CartItem", back_populates="product")
    order_items_rel = db.relationship(
        "OrderItem", backref="associated_product", overlaps="order_items"
    )

    def __repr__(self):
        return f"<Product {self.name}>"

    def reduce_quantity(self, quantity):
        if self.quantity >= quantity:
            self.quantity -= quantity
            db.session.commit()
        else:
            raise ValidationError("Insufficient quantity in stock.")

    def increase_quantity(self, quantity):
        self.quantity += quantity
        db.session.commit()


class Order(db.Model):
    __tablename__ = "order"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")
    total_amount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("OrderItem", back_populates="order")
    user = db.relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Order {self.id}>"

    def __repr__(self):
        return f"<Order id={self.id}, total_amount={self.total_amount}>"

    def get_total_price(self):
        return sum(item.product.price * item.quantity for item in self.items)

    def update_status(self, new_status):
        self.status = new_status
        db.session.commit()

    @staticmethod
    def get_orders_by_user(user_id):
        return Order.query.filter_by(user_id=user_id).all()

    @classmethod
    def create(cls, order, product, quantity):
        if product.quantity >= quantity:
            order_item = cls(order=order, product=product, quantity=quantity)
            product.reduce_quantity(quantity)
            db.session.add(order_item)
            db.session.commit()
        else:
            raise ValidationError("Insufficient quantity in stock.")

    def cancel(self):
        self.product.increase_quantity(self.quantity)
        db.session.delete(self)
        db.session.commit()


class OrderItem(db.Model):
    __tablename__ = "order_item"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product", back_populates="order_items")
   

    def __repr__(self):
        return f"<OrderItem {self.id}>"

    @classmethod
    def create(cls, order, product, quantity):
        if product.quantity >= quantity:
            order_item = cls(order=order, product=product, quantity=quantity)
            product.reduce_quantity(quantity)
            db.session.add(order_item)
            db.session.commit()
        else:
            raise ValidationError("Insufficient quantity in stock.")

    def cancel(self):
        self.product.increase_quantity(self.quantity)
        db.session.delete(self)
        db.session.commit()

    def get_total_price(self):
        return sum(item.product.price * item.quantity for item in self.items)

    def update_status(self, new_status):
        self.status = new_status
        db.session.commit()


class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("CartItem", backref="cart_reference", lazy=True)
    user = db.relationship("User", backref="carts_owned")

    def __repr__(self):
        return f"<Cart {self.id}>"

    def calculate_total_cost(self):
        return sum(item.product.price * item.quantity for item in self.items)

    @staticmethod
    def update_quantity(session, cart_id, product_id, quantity):
        cart_item = CartItem.query.filter_by(
            cart_id=cart_id, product_id=product_id
        ).first()
        if cart_item:
            cart_item.quantity = quantity
            session.commit()

    @staticmethod
    def remove_item(session, cart_id, product_id):
        cart_item = CartItem.query.filter_by(
            cart_id=cart_id, product_id=product_id
        ).first()
        if cart_item:
            session.delete(cart_item)
            session.commit()


class CartItem(db.Model):
    __tablename__ = "cart_item"
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float)

    product = db.relationship("Product", backref="related_cart_items", lazy=True)
    cart = db.relationship("Cart", backref=db.backref("cart_items", lazy=True))

    def __repr__(self):
        return f"<CartItem {self.id}>"

    @property
    def price(self):
        return self.product.price if self.product else None


class Checkout(db.Model):
    __tablename__ = "checkout"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    checkout_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User")
    order = db.relationship("Order")

    def __repr__(self):
        return f"<Checkout {self.id}>"
