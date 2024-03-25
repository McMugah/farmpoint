from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    contact = db.Column(db.Integer(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
