"""
app/helpers.py
Holds users and books decorators and helper functions
"""

from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify, abort
import re

from app.books.models import Genre, BookLog, Book
from app.users.models import UserLog


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


def validate_input(data):
    """
    Validate given book details

    :param data: dict holding book details
    :return: Error message
    """

    genres = ['fiction', 'non-fiction']

    for param in ('title', 'author', 'genre'):
        if param not in data or len(data[param].strip()) < 1 or data['genre'].lower() not in genres:
            return "Invalid " + param

    if 'book_code' not in data:
        return "Missing book Code"
    elif Book.get_book(data['book_code']):
        return "Book(book_code) already in lib"
    elif type(data['book_code']) != int or len(str(data['book_code'])) != 12:
        return "Invalid book_code"

    # Check if given ddc_code follows Dewey Decimal Classification syst.
    if 'ddc_code' not in data:
        return "Missing ddc Code"
    else:
        pattern = r"^[\d][\d][\d](\.*[\d])*$"
        match = re.search(pattern, data['ddc_code'])
        if not match:
            return "Invalid ddc_code. Use DDC structure."


def get_genre(genre):
    """
    Gets genre type from user input
    :param genre: str
    :return:
    """
    if genre == 'fiction':
        return Genre.Fiction
    else:
        return Genre.Non_fiction


def validate_id(book_id):
    """
    check if given book_id is int

    :param book_id: book_id as given in url
    :return: JSON response obj
    """

    if not str(book_id).isdigit():
        abort(400, error="book_id must be a number/integer")
        # return jsonify({"msg": "book_id must be a number/integer"}), 400


def log(recipient, action="INSERT", success=True):
    """
    Updates book log

    :param recipient: book/user entry on which action performed
    :param action: type of action performed on Book entry
    :param success: succes ofaction
    """

    try:
        book = recipient.book_code
        log_table = BookLog
    except AttributeError:
        log_table = UserLoggit

    if not recipient.id:
        success=False

    log_table(recipient.id, action, success).add_to_log()


def verify_username_password(data):
    """
    Verifies that the username and password are valid.

    :param data: holds username and password key-value pairs
    :type data: dict
    :return: invalid input error message
    :rtype: str
    """

    if 'password' not in data or len(data['password'].strip()) < 1:
        return "Invalid Password"

    if 'username' not in data or len(data['username'].strip()) < 1:
        return "Invalid Username"

