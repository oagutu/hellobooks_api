from flask import Blueprint

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/index/')
def indec():
    return "<h1>Hello World</h1>"