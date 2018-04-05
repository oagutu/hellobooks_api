"""
    app/users/routes.py
    Holds book API endpoints.
"""

from flask import Blueprint
from flask import Flask, request, jsonify
import sqlalchemy

from app.users.models import User
from app.books.models import Book 

from datetime import datetime


books_blueprint = Blueprint('books', __name__)

book = Book()
user = User()


@books_blueprint.route('/books', methods=['POST'])
def add_book():
    """
    Adds specified book to library."""

    if request.method == "POST":

        data = request.get_json()
        book_details = {
            "title" : data['title'],
            "author" : data['author'],
            "book_code" : data['book_code'],
            "genre" : data['genre'],
        }
        try:
            if 'status' in data:
                book_info = Book(
                    title=data['title'],
                    author=data['author'],
                    book_code=data['book_code'],
                    genre=data['genre'],
                    synopsis=data['synopsis']
                )
            elif 'subgenre' in data:
                book_info = Book(
                    title=data['title'],
                    author=data['author'],
                    book_code=data['book_code'],
                    genre=data['genre'],
                    synopsis=data['synopsis'],
                    subgenre=data['subgenre']
                )

            else:
                book_info = Book(
                    title=data['title'],
                    author=data['author'],
                    book_code=data['book_code'],
                    genre=data['genre']
                )

            book.save(book_info)

            return jsonify(book_details), 201

        except sqlalchemy.exc.IntegrityError:
            return jsonify({"msg":"Book code already in use"})


@books_blueprint.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Updates book entry in library."""

    if request.method == "PUT":

        data = request.get_json()

        try:
            library = book.get_all_books()
            del library[book_id]

            book_info = [
                data['book_id'],
                data['title'],
                data['author'],
                data['book_code'],
                data['synopsis'],
                data['genre'],
                data['subgenre'],
                data['status']
            ]

            book_details = book.set_book(book_info)

            return jsonify(book_details), 202


        except KeyError:
            book_details = {"msg" : "Book entry not available"}

            return jsonify(book_details), 404


@books_blueprint.route('/books/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    """
    Delete book entry from library."""

    if request.method == 'DELETE':

        try:
            library = book.get_all_books()
            del library[book_id]

            book_details = {"msg" : "Book entry deleted"}

            return jsonify(book_details), 204

        except KeyError:
            book_details = {"msg" : "Book entry not available"}

            return jsonify(book_details), 404


@books_blueprint.route('/books', methods=['GET'])
def retrieve_all_books():
    """
    Retieves all books in library."""

    if request.method == 'GET':

        library = book.get_all_books()
        return jsonify(library), 200


@books_blueprint.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Gets specific book using book_id."""

    if request.method == 'GET':

        try:
            book_details = book.get_book(book_id)

            return jsonify(book_details), 200

        except KeyError:

            return jsonify({"msg" : "Book not avialable"}), 404


@books_blueprint.route('/users/books/<int:book_id>', methods=['POST'])
def borrow_return_book(book_id):
    """
    Allows borrowing/returning of books."""

    if request.method == 'POST':
        data = request.get_json()

        book_info = {}
        try:
            book_details = book.get_book(book_id)
            book_status = book_details["status"]
            if data["acc_status"] == "member" and book_status == "available":

                book_info = user.set_borrowed()
                book_info["book_id"] = book_id
                book_info["borrower_id"] = data["user_id"]
                user.add_to_borrowed(book_id, book_info)

                book.get_book(book_id)["status"] = "borrowed"
                book_info['status'] = "borrowed"

                return jsonify(book_info), 201

            elif data["acc_status"] == "member" and book_status == "borrowed":
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
                        "msg" : "cannot return book. Not borrowed by user",
                        "status" : "borrowed"})

            elif data["acc_status"] != "member":

                return jsonify(
                    {
                        "msg" : "Member currently not authorised to borrow book"})

        except KeyError:

            return jsonify({"msg" : "Book not avialable"}), 404
