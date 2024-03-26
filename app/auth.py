from functools import wraps

from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from .models import User

auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@auth.error_handler
def unauthorized():
    response = jsonify({"message": "Unauthorized access"})
    response.status_code = 401
    response.headers["WWW-Authenticate"] = 'Basic realm="Login Required"'
    return response


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not auth.current_user:
            return unauthorized()
        return f(*args, **kwargs)

    return decorated_function


@token_auth.verify_token
def verify_token(token):
    user = User.verify_token(token)
    if user:
        g.user = user
        return True
    return False


@token_auth.error_handler
def token_unauthorized():
    response = jsonify({"message": "Unauthorized access"})
    response.status_code = 401
    return response


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return unauthorized()
        token = token.split(" ")[1]
        user = User.verify_token(token)
        if not user:
            return unauthorized()
        g.user = user
        return f(*args, **kwargs)

    return decorated_function
