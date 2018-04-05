'''app/__init__.py'''

from flask import render_template
from flask_api import FlaskAPI
from flask_jwt_extended import JWTManager


from config import app_config


def create_app(config_name):
    """
    Creates instance of flask app."""

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['JWT_SECRET_KEY'] = '8gf%bw72biu2789)8h31hiuwefgonmOI$%N@@MP'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    jwt = JWTManager(app)

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
