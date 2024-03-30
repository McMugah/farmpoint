from flask import redirect, request, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app import db
from app.models import Cart, CartItem, Order, OrderItem, Product, User


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login", next=request.url))


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login", next=request.url))


def create_admin_panel(app):
    admin = Admin(app, index_view=MyAdminIndexView())
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Cart, db.session))
    admin.add_view(MyModelView(Product, db.session))
    admin.add_view(MyModelView(Order, db.session))
    admin.add_view(MyModelView(OrderItem, db.session))
    admin.add_view(MyModelView(CartItem, db.session))
