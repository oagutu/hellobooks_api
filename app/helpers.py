"""
app/helpers.py
Holds users and books decorators and helper functions
"""

from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify


def already_logged_in(fn):
    """
    Check if user already logged in

    :param fn: login func
    :return: wrapper func
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        """
        check if user logged in

        :param args: endpoint arguments
        :param kwargs: endpoint arguments
        :return: endpoint  or error message
        :rtype: func or json obj
        """

        if not get_jwt_identity():
            return fn(*args, **kwargs)
        else:
            msg = "Already logged in as: " + get_jwt_identity()
            return jsonify({"msg": msg})

    return wrapper
