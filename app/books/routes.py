"""
    app/users/routes.py
    Hold books API endpoints.
"""

from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

import re
from app.books.models import Genre


from app.users.models import User
from app.books.models import Book, BookLog, BorrowedBook
from app.blacklist.helpers import admin_required, verify_status


from datetime import datetime, timedelta

books_blueprint = Blueprint('books', __name__)


@books_blueprint.route('/books', methods=['POST'])
@jwt_required
@admin_required
def add_book():
    """Add specified book to library."""

    data = request.get_json()

    if 'title' not in data or len(data['title'].strip()) < 1:
        return jsonify({"msg": "Invalid title"}), 400

    if 'author' not in data or len(data['author'].strip()) < 1:
        return jsonify({"msg": "Invalid author"}), 400
    genres = ['fiction', 'non-fiction']
    if 'genre' not in data or data['genre'].lower() not in genres:
        return jsonify({"msg": "Invalid genre"})

    if 'book_code' not in data:
        return jsonify({"msg": "Missing book Code"}), 400
    elif Book.get_book(data['book_code']):
        return jsonify({"msg": "Book(book_code) already in lib"}), 409

    # Checks if given ddc_code follows Dewey Decimal Classification syst.
    if 'ddc_code' not in data:
        return jsonify({"msg": "Missing ddc Code"}), 400
    else:
        pattern = r"^[\d][\d][\d](\.*[\d])*$"
        match = re.search(pattern, data['ddc_code'])
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


@books_blueprint.route('/books/<int:book_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_book(book_id):
    """
    Update book entry in library

    :param book_id: id of book to be updated.
    :type book_id: int
    :return: updated book entry.
    :rtype: JSON obj
    """

    data = request.get_json()

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


@books_blueprint.route('/books/<int:book_id>', methods=['DELETE'])
@jwt_required
@admin_required
def remove_book(book_id):
    """
    Delete book entry from library.

    :param book_id: id of book to be deleted form db
    :type book_id: int
    :return: message on result of deletion
    :rtype: JSON obj
    """

    try:
        book = Book.get_book(book_id)
        book.delete_book()

        if not Book.get_book(book.id):
            BookLog(book.id, action='DELETE').add_to_log()
        else:
            BookLog(book.id, action='DELETE', success=False).add_to_log()

        book_details = {"msg": "Book entry deleted"}

        return jsonify(book_details), 204

    except AttributeError:
        book_details = {"msg": "Book entry not available"}

        return jsonify(book_details), 404


@books_blueprint.route('/books', methods=['GET'])
@jwt_required
def retrieve_all_books():
    """
    Retrieve all books in library.

    :return: all books in the library db
    :rtype: JSON obj
    """

    entry_no = request.args.get('results')
    page = request.args.get('page')

    if entry_no and page:
        all_books = Book.get_all_books(int(entry_no), int(page))

    elif entry_no and not page:
        page = 1
        all_books = Book.get_all_books(int(entry_no), page)

    elif not entry_no and page:
        entry_no = 3
        all_books = Book.get_all_books(entry_no, int(page))

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
    Get specific book using book_id.

    :param book_id: id of book to be fetched
    :type book_id: int
    :return: specified book details
    :rtype: JSON obj
    """

    if Book.get_book(book_id):
        book_details = Book.get_book(book_id)
        # print('test point: book details\n: ', book_details)

        return jsonify({
            "book_id": book_details.id,
            "title": book_details.title,
            "author": book_details.author,
            "book_code": book_details.book_code,
            "genre": book_details.genre.value,
            "sub)genre": book_details.sub_genre,
            "synopsis": book_details.synopsis}), 200
    else:
        return jsonify({"msg": "Book not available"}), 404


@books_blueprint.route('/users/books/<int:book_id>', methods=['POST', 'PUT'])
@jwt_required
@verify_status
def borrow_return_book(book_id):
    """
    Facilitate borrowing/returning of books.

    :param book_id: id of book to be borrowed/returned
    :type book_id: int
    :return: json obj containing status message or borrowed/returned book details
    :rtype: JSON obj
    """

    try:
        user = User.get_user(get_jwt_identity())
        book_details = Book.get_book(book_id)
        book_status = book_details.status

        # Borrow available book by authorised user.
        if request.method == 'POST' and book_status == "available":

            borrow = BorrowedBook(book_id, user.id)
            borrow.save()
            book_details.set_book_status("borrowed")

            return jsonify({
                "book_id": borrow.book_id,
                "borrow_date": borrow.borrow_date,
                "due_date":  (datetime.now() + timedelta(days=10)).strftime("%d/%m/%Y %H:%M"),
                "return_date": borrow.return_date,
                "status": borrow.status,
                "fee_owed": borrow.fee_owed
            }), 201

        elif request.method == "POST" and book_status == "borrowed":
            return jsonify({"msg": "Book not available for borrowing"})

        # Return borrowed book by authorised user.
        elif request.method == 'PUT' and book_status == "borrowed":

            try:
                borrowed_book = BorrowedBook.get_borrowed_by_id(book_id)
                current_date = datetime.now()
                borrow_date = borrowed_book.borrow_date
                expected_return_date = (borrow_date + timedelta(days=10)).strftime("%d/%m/%Y %H:%M")
                expected_return_date = datetime.strptime(expected_return_date, "%d/%m/%Y %H:%M")
                borrow_period = str(current_date - expected_return_date).split(' ')[0]
                if type(borrow_period) != int:
                    borrow_period = 0
                else:
                    borrow_period = int(borrow_period)

                borrowed_book.update_borrowed(borrow_period)
                borrowed_book.save()
                book_details.set_book_status("available")

                return jsonify({
                    "book_id": borrowed_book.book_id,
                    "borrow_date": borrowed_book.borrow_date,
                    "return_date": borrowed_book.return_date,
                    "fee_owed": borrowed_book.fee_owed,
                    "status": borrowed_book.status
                }), 202

            except AttributeError:
                return jsonify({
                        "msg": "cannot return book. Not borrowed by user",
                        "book_status": "borrowed"})

        elif request.method == 'PUT' and book_status == 'available':
            return jsonify({"msg": "Book already available"})

    except AttributeError:

        return jsonify({"msg": "Book not available"}), 404


@books_blueprint.route('/users/books', methods=['GET'])
@jwt_required
def get_borrow_history():
    """
    Enable viewing of borrow history.

    :return: users borrowed books details
    :rtype: JSON obj
    """

    returned = request.args.get("returned")
    order_param = request.args.get("order_param")

    user = User.get_user(get_jwt_identity())
    if order_param:
        borrowed_books = BorrowedBook.get_borrowed(user.id, order_param)
    elif returned and not order_param:
        borrowed_books = BorrowedBook.get_borrowed(user.id, 'borrow_date', False)
    else:
        borrowed_books = BorrowedBook.get_borrowed(user.id)

    borrowed = []
    for book in borrowed_books:
        entry = {
            "book_id": book.book_id,
            "book_title": book.book.title,
            "borrow_date": book.borrow_date,
            "return_date": book.return_date,
            "fee_owed": book.return_date
        }
        borrowed.append(entry)

    return jsonify(borrowed), 200


@books_blueprint.route('/users/books/logs', methods=['GET'])
@jwt_required
@admin_required
def get_log():
    """
    Enable viewing of book logs.

    :return: log of all changes made to the books table
    :rtype: JSON obj
    """

    book_id = request.args.get("book_id")

    if book_id:
        logs = BookLog.get_logs(int(book_id))
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
