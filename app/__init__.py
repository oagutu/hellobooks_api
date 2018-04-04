'''app/__init__.py'''

from flask import render_template
from flask_api import FlaskAPI


from config import app_config

from datetime import datetime, timedelta


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    @app.route('/')
    def index():
        '''loads up documentation.html as app landing page'''
        return render_template('documentation.html')

    from app.users.routes import users_blueprint
    from app.books.routes import books_blueprint

    app.register_blueprint(books_blueprint, url_prefix='/api/v1')
    app.register_blueprint(users_blueprint,  url_prefix='/api/v1/auth')

    return app
