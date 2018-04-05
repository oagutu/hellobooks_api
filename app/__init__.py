'''app/__init__.py'''

from flask import render_template
from flask_api import FlaskAPI

from flask_sqlalchemy import SQLAlchemy


from config import app_config

db = SQLAlchemy()

def create_app(config_name):
    """
    Creates instance of flask app."""

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    db.init_app(app)

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
