from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Development")
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from .api_v1 import api

    app.register_blueprint(api, url_prefix="/api")

    from .admin.admin import create_admin_panel

    create_admin_panel(app)

    return app
