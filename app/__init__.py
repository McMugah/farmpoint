from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


login_manager = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()



def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Development")
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    from .api_v1 import api as api_blueprint
    app.register_blueprint(api_blueprint)


    return app
