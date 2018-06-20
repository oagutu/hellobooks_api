"""
app/__init__.py
Creates new app and loads config settings."""

from flask import render_template
from flask_api import FlaskAPI
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

from config import app_config

db = SQLAlchemy()


def create_app(config_name):
    """
    Creates instance of flask app."""

    app = FlaskAPI(__name__)
    app.config.from_object(app_config[config_name])

    app.config['JWT_SECRET_KEY'] = '8gf%bw72biu2789)8h31hiuwefgonmOI$%N@@MP'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=25)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    jwt = JWTManager(app)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    blacklist = set()

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist

    @app.route('/')
    def index():
        """
        Loads up documentation.html as app landing page."""

        return render_template('documentation.html')

    from app.users.routes import users_blueprint
    from app.books.routes import books_blueprint

    app.register_blueprint(books_blueprint, url_prefix='/api/v1')
    app.register_blueprint(users_blueprint,  url_prefix='/api/v1/auth')

    return app
