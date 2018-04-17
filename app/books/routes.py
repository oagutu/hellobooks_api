"""
    app/users/routes.py
    Holds book API endpoints.
"""

from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

import re

from app.users.models import User
from app.books.models import Book 

from datetime import datetime

books_blueprint = Blueprint('books', __name__)

book = Book()
user = User()


@books_blueprint.route('/books', methods=['POST'])
@jwt_required
def add_book():
    """
    Adds specified book to library."""

    try:
        acc = user.get_user(get_jwt_identity())

        if request.method == "POST" and acc["acc_status"] == "admin":

            data = request.get_json()

            if len(data['title'].strip()) < 1:
                return jsonify({"msg": "Invalid title"}), 400

            if len(data['author'].strip()) < 1:
                return jsonify({"msg": "Invalid author"}), 400

            print(data)
            # Checks if given book code follows Dewey Decimal Classification.
            pattern = r"^[\d][\d][\d](\.*[\d])*$"
            match = re.search(pattern, data['book_code'])
            if not match:
                return jsonify({"msg": "Invalid book code. Use DDC standards."}), 400

            book_info = {
                "book_id": data['book_id'],
                "title": data['title'],
                "author": data['author'],
                "book_code": data['book_code'],
                "genre": data['genre']
            }
            if "synopsis" in data:
                book_info["synopsis"] = data["synopsis"]

            if "subgenre" in data:
                book_info["subgenre"] = data["subgenre"]

            book_details = book.set_book(book_info)

            return jsonify(book_details), 201

        else:
            return jsonify({"msg": "Account not authorised to perform selected function"})
    except KeyError:
        return jsonify({"msg": "user account unavailable"})


@books_blueprint.route('/books/<int:book_id>', methods=['PUT'])
@jwt_required
def update_book(book_id):
    """
    Updates book entry in library."""

    acc_type = user.get_user(get_jwt_identity())

    if request.method == "PUT" and acc_type["acc_status"] == "admin":

        data = request.get_json()

        try:
            library = book.get_all_books()
            del library[book_id]

            book_info = {
                "book_id": data['book_id'],
                "title": data['title'],
                "author": data['author'],
                "book_code": data['book_code'],
                "genre": data['genre']
            }
            if data["synopsis"]:
                book_info["synopsis"] = data["synopsis"]
            if data["subgenre"]:
                book_info["subgenre"] = data["subgenre"]

            book_details = book.set_book(book_info)

            return jsonify(book_details), 202

        except KeyError:
            book_details = {"msg": "Book entry not available"}

            return jsonify(book_details), 404


@books_blueprint.route('/books/<int:book_id>', methods=['DELETE'])
@jwt_required
def remove_book(book_id):
    """
    Delete book entry from library."""

    acc_type = user.get_user(get_jwt_identity())

    if request.method == 'DELETE' and acc_type["acc_status"] == "admin":

        try:
            library = book.get_all_books()
            del library[book_id]

            book_details = {"msg": "Book entry deleted"}

            return jsonify(book_details), 204

        except KeyError:
            book_details = {"msg": "Book entry not available"}

            return jsonify(book_details), 404


@books_blueprint.route('/books', methods=['GET'])
@jwt_required
def retrieve_all_books():
    """
    Retieves all books in library."""

    if request.method == 'GET':

        library = book.get_all_books()
        return jsonify(library), 200


@books_blueprint.route('/books/<int:book_id>', methods=['GET'])
@jwt_required
def get_book(book_id):
    """
    Gets specific book using book_id."""

    if request.method == 'GET':

        try:
            book_details = book.get_book(book_id)

            return jsonify(book_details), 200

        except KeyError:

            return jsonify({"msg": "Book not avialable"}), 404


@books_blueprint.route('/users/books/<int:book_id>', methods=['POST'])
@jwt_required
def borrow_return_book(book_id):
    """
    Allows borrowing/returning of books."""

    if request.method == 'POST':
        data = request.get_json()

        book_info = {}
        try:
            acc = user.get_user(get_jwt_identity())
            book_details = book.get_book(book_id)
            book_status = book_details["status"]
            if acc["acc_status"] != "suspended" and book_status == "available":

                book_info = user.set_borrowed()
                book_info["book_id"] = book_id
                book_info["borrower_id"] = acc["user_id"]
                user.add_to_borrowed(book_id, book_info)

                book.get_book(book_id)["status"] = "borrowed"
                book_info['status'] = "borrowed"

                return jsonify(book_info), 201

            elif acc["acc_status"] != "suspended" and book_status == "borrowed":
                if book_id in user.borrowed_books:
                    borrowed_book = user.borrowed_books[book_id]
                    current_day = datetime.now()
                    return_day = datetime.strptime(
                        borrowed_book["return_date"],  '%d/%m/%Y %H:%M')
                    borrow_period = int(
                        str(current_day - return_day).split(' ')[0])
                    if borrow_period > 0:
                        borrowed_book["fee_owed"] = borrow_period * 30
                        borrowed_book["borrow_status"] = "unreturned"

                    book.get_book(book_id)["status"] = "returned"
                    borrowed_book["status"] = "returned"

                    return jsonify(borrowed_book)

                return jsonify(
                    {
                        "msg": "cannot return book. Not borrowed by user",
                        "status": "borrowed"})

            elif acc["acc_status"] == "suspended":

                return jsonify(
                    {
                        "msg": "Member currently not authorised to borrow book"})

        except KeyError:

            return jsonify({"msg": "Book not available"}), 404
