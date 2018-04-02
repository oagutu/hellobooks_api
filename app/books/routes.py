'''
    app/users/routes.py
    Holds book API endpoints
'''

from flask import Blueprint
from flask import Flask, request, jsonify

from app.models import User, Book

from datetime import datetime



books_blueprint = Blueprint('books', __name__)

book = Book()
user = User()

@books_blueprint.route('/books', methods=['POST'])
def add_book():
    '''adds specified book to library'''

    if request.method == "POST":

        data = request.get_json()
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
        #returns dictionary with book details

        response = jsonify(book_details)

        response.status_code = 201

        return response

@books_blueprint.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    '''updates book entry in library'''

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

            response = jsonify(book_details)

            response.status_code = 202

            return response

        except KeyError:
            book_details = {"msg": "Book entry not available"}

            response = jsonify(book_details)
            response.status_code = 404

            return response

@books_blueprint.route('/books/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    '''delete book entry from library'''

    if request.method == 'DELETE':

        try:
            library = book.get_all_books()
            del library[book_id]

            book_details = {"msg": "Book entry deleted"}

            response = jsonify(book_details)
            response.status_code = 200

            return response

        except KeyError:
            book_details = {"msg": "Book entry not available"}

            response = jsonify(book_details)
            response.status_code = 404

            return response

@books_blueprint.route('/books', methods=['GET'])
def retrieve_all_books():
    '''retieves all books in library'''

    if request.method == 'GET':

        library = book.get_all_books()
        response = jsonify(library)

        response.status_code = 200

        return response

@books_blueprint.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    '''gets specific book using book_id'''

    if request.method == 'GET':

        try:
            book_details = book.get_book(book_id)

            response = jsonify(book_details)
            response.status_code = 200

            return response

        except KeyError:
            response = jsonify({"msg": "Book not avialable"})
            response.status_code = 404

            return response

@books_blueprint.route('/users/books/<int:book_id>', methods=['POST'])
def borrow_return_book(book_id):
    '''allows borrowing/returning of books'''

    if request.method == 'POST':
        data = request.get_json()

        book_info = {}
        try:
            book_details = book.get_book(book_id)
            book_status = book_details["status"]
            if data["acc_status"] == "member" and book_status == "available":

                book_info = user.set_borrowed(book_status, book_id)
                book_info["book_id"] = book_id
                book_info["borrower_id"] = data["user_id"]
                user.add_to_borrowed(book_id, book_info)

                book.get_book(book_id)["status"] = "borrowed"
                book_info['status'] = "borrowed"

                response = jsonify(book_info)
                response.status_code = 201

                return response

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
                    response = jsonify(borrowed_book)

                    return response

                response = jsonify(
                    {"msg": "Book not available for borrowing",
                        "status": "borrowed"})

                return response

            elif data["acc_status"] != "member":
                response = jsonify(
                    {"msg": "Member currently not authorised to borrow book"})

                return response

        except KeyError:
            response = jsonify({"msg": "Book not avialable"})
            response.status_code = 404

            return response
