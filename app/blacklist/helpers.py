"""
app/blacklist/helpers.py
Holds blacklist decorators
"""

from functools import wraps
from flask_jwt_extended import get_jwt_claims
from flask import jsonify

from app.blacklist.models import Blacklist


# Limits endpoint access to admins.'
def admin_required(fn):
    """
    Limit access to endpoint to admins

    :param fn: endpoint func to be accessed
    :return: wrapper function
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        """
        Verify admin user role.
        :param args: endpoint arguments
        :param kwargs: endpoint arguments
        :return: endpoint  or error message
        :rtype: func or json obj
        """

        if get_jwt_claims()['role'] == 'admin':
            return fn(*args, **kwargs)
        else:
            return jsonify({'msg': 'Unauthorised User'}), 403

    return wrapper


# Check if user account status is valid
def verify_status(fn):
    """
    Check if user account status not suspended or banned

    :param fn: endpoint func to be accessed
    :return: endpoint or error message
    :rtype: wrapper func
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        """
        Checks account status before endpoint accessed
        :param args: endpoint arguments
        :param kwargs: endpoint arguments
        :return: func or json obj
        """

        if get_jwt_claims()['role'] not in ['suspended', 'banned']:
            return fn(*args, **kwargs)
        else:
            return jsonify(
                {"msg": "Member currently not authorised to borrow book"}), 403

    return wrapper


def check_blacklist(token):
    """Check if token in blacklist"""

    if Blacklist.get_token(token['jti']):
        return True
    else:
        return False
