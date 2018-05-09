"""
    app/users/routes.py
    Holds book API endpoints.
"""

from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from math import ceil
import re
from app.books.models import Genre


from app.users.models import User
from app.books.models import Book, BookLog

from datetime import datetime

books_blueprint = Blueprint('books', __name__)


@books_blueprint.route('/books', methods=['POST'])
@jwt_required
def add_book():
    """
    Adds specified book to library."""

    acc = User.get_user(get_jwt_identity())

    if request.method == "POST" and acc.acc_status == "admin":

        data = request.get_json()

        if len(data['title'].strip()) < 1:
            return jsonify({"msg": "Invalid title"}), 400

        if len(data['author'].strip()) < 1:
            return jsonify({"msg": "Invalid author"}), 400

        if 'book_code' not in data:
            return jsonify({"msg": "Missing book Code"}), 400
        elif Book.get_book(data['book_code']):
            # print(Book.get_book(data['book_code']))
            return jsonify({"msg": "Book(book_code) already in lib"}), 409

        # Checks if given ddc_code follows Dewey Decimal Classification syst.
        # print(data)
        if 'ddc_code' not in data:
            # print(data)
            return jsonify({"msg": "Missing ddc Code"}), 400
        else:
            pattern = r"^[\d][\d][\d](\.*[\d])*$"
            match = re.search(pattern, data['ddc_code'])
            # print(match)
            if not match:
                return jsonify({"msg": "Invalid ddc_code. Use DDC structure."}), 400

        if type(data['book_code']) != int or len(str(data['book_code'])) != 12:
            return jsonify({"msg": "Invalid book_code"}), 400

        book_info = {
            "title": data['title'],
            "author": data['author'],
            "book_code": data['book_code'],
            "ddc_code": data['ddc_code'],
        }
        if data['genre'] == 'fiction':
            book_info['genre'] = Genre.Fiction
        else:
            book_info['genre'] = Genre.Non_fiction

        if 'book_id' in data:
            book_info['book_id'] = data['book_id']

        if "synopsis" in data:
            book_info["synopsis"] = data["synopsis"]

        if "subgenre" in data:
            book_info["subgenre"] = data["subgenre"]

        if 'status' in data:
            book_info["status"] = data["status"]

        book = Book(book_info)
        book.add_to_lib()
        if book.id:
            BookLog(book.id).add_to_log()
        else:
            BookLog(book.id, success=False).add_to_log()

        return jsonify({
            "book_id": book.id,
            "title": book.title,
            "author": book.author,
            "book_code": book.book_code,
            "ddc_code": book.ddc_code,
            "genre": book.genre.value,
            "sub_genre": book.sub_genre,
            "synopsis": book.synopsis
            }), 201
    else:
        return jsonify({"msg": "Account not authorised to perform selected function"}), 401


@books_blueprint.route('/books/<int:book_id>', methods=['PUT'])
@jwt_required
def update_book(book_id):
    """
    Updates book entry in library."""

    acc = User.get_user(get_jwt_identity())

    if request.method == "PUT" and acc.acc_status == "admin":

        data = request.get_json()
        # print(data)

        try:
            book = Book.get_book(book_id)
            book.delete_book()
            book_info = {}
            for val in data:
                if val == 'genre':
                    if data['genre'] == 'fiction':
                        book_info['genre'] = Genre.Fiction
                    else:
                        book_info['genre'] = Genre.Non_fiction
                else:
                    book_info[val] = data[val]
            book_info['book_id'] = book_id
            book = Book(book_info)
            book.add_to_lib()

            if book.id:
                BookLog(book.id, action='UPDATE').add_to_log()
            else:
                BookLog(book.id, action='UPDATE', success=False).add_to_log()

            return jsonify({
                "book_id": book.id,
                "title": book.title,
                "author": book.author,
                "book_code": book.book_code,
                "ddc_code": book.ddc_code,
                "genre": book.genre.value,
                "sub_genre": book.sub_genre,
                "synopsis": book.synopsis
            }), 202

        except AttributeError:
            book_details = {"msg": "Book entry not available"}

            return jsonify(book_details), 404
    else:
        return jsonify({"msg": "Account not authorised to perform selected function"}), 401


@books_blueprint.route('/books/<int:book_id>', methods=['DELETE'])
@jwt_required
def remove_book(book_id):
    """
    Delete book entry from library."""

    acc_type = User.get_user(get_jwt_identity())

    if request.method == 'DELETE' and acc_type.acc_status == "admin":

        try:
            book = Book.get_book(book_id)
            book.delete_book()

            if not book.id:
                BookLog(book.id, action='DELETE').add_to_log()
            else:
                BookLog(book.id, action='DELETE', success=False).add_to_log()

            book_details = {"msg": "Book entry deleted"}

            return jsonify(book_details), 204

        except AttributeError:
            book_details = {"msg": "Book entry not available"}

            return jsonify(book_details), 404
    else:
        return jsonify({"msg": "Account not authorised to perform selected function"}), 401


@books_blueprint.route('/books', methods=['GET'])
@jwt_required
def retrieve_all_books():
    """
    Retieves all books in library."""

    if request.method == 'GET':

        entry_no = request.args.get('results')
        page = request.args.get('page')
        if entry_no and page:
            all_books = Book.get_all_books(entry_no, int(page))

        elif entry_no and not page:
            all_books = Book.get_all_books(entry_no)

        elif not entry_no and page:
            all_books = Book.get_all_books(int(page))

        else:
            all_books = Book.get_all_books()
        library = {}

        for book in all_books:
            entry = {
                "book_id": book.id,
                "title": book.title,
                "author": book.author,
                "book_code": book.book_code,
                "ddc_code": book.ddc_code,
                "genre": book.genre.value,
                "sub_genre": book.sub_genre,
                "synopsis": book.synopsis
            }
            library[book.id] = entry

        return jsonify(library), 200


@books_blueprint.route('/books/<int:book_id>', methods=['GET'])
@jwt_required
def get_book(book_id):
    """
    Gets specific book using book_id."""

    if request.method == 'GET':

        if Book.get_book(book_id):
            book_details = Book.get_book(book_id)
            print('test point: book details\n: ', book_details)

            return jsonify({
                "book_id": book_details.id,
                "title": book_details.title,
                "author": book_details.author,
                "book_code": book_details.book_code,
                "genre": book_details.genre.value,
                "sub)genre": book_details.sub_genre,
                "synopsis": book_details.synopsis}), 200
        else:
            # print('test point: bk not available')
            return jsonify({"msg": "Book not available"}), 404


@books_blueprint.route('/users/books/<int:book_id>', methods=['POST', 'PUT'])
@jwt_required
def borrow_return_book(book_id):
    """
    Allows borrowing/returning of books."""

    try:
        user = User.get_user(get_jwt_identity())
        # print(user.acc_status)
        # print(user.get_all_borrowed())
        book_details = Book.get_book(book_id)
        # print("TP - Borrow:\n", book_details)
        book_status = book_details.status
        # Borrow available book by authorised user.

        if user.acc_status == "suspended":

            return jsonify(
                {
                    "msg": "Member currently not authorised to borrow book"}), 401

        if request.method == 'POST':
            if user.acc_status != "suspended" and book_status == "available":

                borrow_info = user.set_borrowed()
                # print("TP - Borrow Info:\n ", borrow_info)
                borrow_info["book_id"] = book_id
                user.add_to_borrowed(book_id, borrow_info)

                book_details.set_book_status("borrowed")

                borrowed_book = {
                    "book_id": book_details.id,
                    "book_code": book_details.book_code,
                    "title": book_details.title,
                    "status": book_details.status
                }

                borrow_info.update(borrowed_book)

                return jsonify(borrow_info), 201

        # Return borrowed book by authorised user.
        elif request.method == 'PUT':

            if user.acc_status != "suspended" and book_status == "borrowed":
                # print(user.borrowed_books)
                if str(book_id) in user.borrowed_books:
                    borrowed_book = user.borrowed_books[str(book_id)]
                    # print(user.borrowed_books)
                    current_day = datetime.now()
                    return_day = datetime.strptime(
                        borrowed_book["ERD"],  '%d/%m/%Y %H:%M')
                    borrow_period = str(current_day - return_day).split(' ')[0]
                    if type(borrow_period) != int:
                        borrow_period = 0
                    else:
                        borrow_period = int(borrow_period)
                    user.update_borrowed(str(book_id), borrow_period)

                    return jsonify(borrowed_book), 202

                else:
                    return jsonify(
                        {
                            "msg": "cannot return book. Not borrowed by user",
                            "book_status": "borrowed"})

    except AttributeError:

        return jsonify({"msg": "Book not available"}), 404


@books_blueprint.route('/users/books', methods=['GET'])
@jwt_required
def get_borrow_history():
    """
    Enables viewing of borrow history."""

    if request.method == 'GET':
        returned = request.args.get("returned")
        entries = request.args.get("results")
        order_param = request.args.get("order_param")

        user = User.get_user(get_jwt_identity())
        if order_param:
            borrowed_books, record_details = user.get_all_borrowed(False, order_param)
        else:
            borrowed_books, record_details = user.get_all_borrowed()

        # print("TP1 - borrow details: \n", borrowed_books)

        if not returned:
            for key in borrowed_books:
                current_day = datetime.now()
                return_day = datetime.strptime(
                    borrowed_books[key]['ERD'],  '%d/%m/%Y %H:%M')
                borrow_period = str(current_day - return_day).split(' ')[0]
                if current_day <= return_day:
                    borrow_period = 0
                else:
                    borrow_period = int(borrow_period)

                user.update_borrowed(str(key), borrow_period, True)
                # print("{0} \n {1} ".format(key, user.get_all_borrowed()[0]))

                if entries:
                    entries = int(entries)
                    record_details['tot_pages'] = ceil(record_details['records']/entries)
                    keys = record_details['keys'][:(entries + 1)]
                    borrowed_temp = {}
                    for val in keys:
                        borrowed_temp[val] = borrowed_books[val]
                    borrowed_books = borrowed_temp

            # print(borrowed_books, record_details)
            print(user.get_all_borrowed())
            return jsonify(borrowed_books), 200

        elif returned == 'false':
            pending_books = {}
            for key in borrowed_books:
                if borrowed_books[key]['borrow_status'] == 'invalid':
                    pending_books[key] = borrowed_books[key]

            return jsonify(pending_books), 200


@books_blueprint.route('/users/books/logs', methods=['GET'])
@jwt_required
def get_log():
    """
    Enables viewing of book logs."""

    acc_type = User.get_user(get_jwt_identity())
    book_id = request.args.get("book_id")

    if request.method == 'GET' and acc_type.acc_status == "admin":
        if book_id:
            logs = BookLog.get_logs(book_id)
        else:
            logs = BookLog.get_logs()

        audit_log = {}
        for log in logs:
            entry = {
                "book_id": log.book_id,
                "timestamp": log.timestamp,
                "action": log.action,
                "success": log.success
                }
            audit_log[log.log_id] = entry

        return jsonify(audit_log), 200
    else:
        return jsonify({'msg': 'User not authorised'}), 401
