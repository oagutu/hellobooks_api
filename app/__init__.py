'''app/__init__.py'''

from flask_api import FlaskAPI
from flask import Flask, request, jsonify, session, flash

from config import app_config
from app.models import User, Book

from datetime import datetime, timedelta


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    from app.users.routes import users_blueprint
    from app.books.routes import books_blueprint

    app.register_blueprint(books_blueprint, url_prefix='/api/v1')
    app.register_blueprint(users_blueprint) 


    return app
