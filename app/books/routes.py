"""
    app/users/routes.py
    Hold books API endpoints.
"""

from flask import Blueprint
from flask import request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)

from app.users.models import User
from app.books.models import Book, BookLog, BorrowedBook
from app.blacklist.helpers import admin_required, verify_status
from app.helpers import get_genre, log, validate_input

from datetime import datetime, timedelta

books_blueprint = Blueprint('books', __name__)


@books_blueprint.route('/books', methods=['POST'])
@jwt_required
@admin_required
def add_book():
    """Add specified book to library."""

    data = request.get_json()

    invalid_msg = validate_input(data)
    if invalid_msg:
        return jsonify({"msg": invalid_msg}), 400

    book_info = {}

    for param in ('title', 'author', 'book_code', 'ddc_code', 'book_id', 'synopsis', 'subgenre', 'status', "genre"):
        if param in data and param == "genre":
            book_info['genre'] = get_genre(data["genre"])
        elif param in data:
            book_info[param] = data[param]

    book = Book(book_info)
    book.add_to_lib()
    log(book)

    return jsonify({"msg": "Successfully added book", "book": book.book_serializer()}), 201


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

        if "book_code" and Book.get_book(data["book_code"]) and Book.get_book(data["book_code"]) != book:
            return jsonify({"msg": "Book code already in use"}), 400

        book.genre = get_genre(data['genre'])
        book.sub_genre = data['genre']
        book.synopsis = data['synopsis']
        book.title = data['title']
        book.author = data['author']
        book.book_code = data['book_code']
        book.ddc_code = data['ddc_code']

        book.update()
        log(book, 'UPDATE')

        return jsonify({"msg": "Successfully updated book", "book": book.book_serializer()}), 202

    except AttributeError:
        return jsonify({"msg": "Book entry not available"}), 404


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
        if BorrowedBook.query.filter_by(book_id=book_id, return_date=None).first():
            return jsonify({"msg": "Book entry cannot be deleted as it currently borrowed."}), 403
        book = Book.get_book(book_id)
        book.delete_book()
        log(book, 'DELETE')

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

    results = request.args.get('results')
    page = request.args.get('page')

    if not results:
        results = 10
    if not page:
        page = 1

    all_books = Book.get_all_books(int(results), int(page))
    library = {"books": []}

    for book in all_books.items:
        entry = book.book_serializer()
        library["books"].append(entry)

    prev_pg = int(page)
    next_pg = int(page)
    if all_books.has_prev:
        prev_pg = all_books.prev_num
    if all_books.has_next:
        next_pg = all_books.next_num

    library.update({
        "no_of_results": len(library["books"]),
        "prev_page": prev_pg,
        "prev_url": request.path + "?page=" + str(prev_pg) + "&results=" + str(results),
        "next_page": next_pg,
        "next_url": request.path + "?page=" + str(next_pg) + "&results=" + str(results)
    })
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

        return jsonify(book_details.book_serializer())

    else:
        return jsonify({"msg": "Book not available"}), 404


@books_blueprint.route('/books/search', methods=['GET'])
@jwt_required
def search():
    """
    Search for book by title/author.

    :return: queried book details
    """
    search_param = request.args.get("q")
    try:
        if search_param:
            books = Book.get_book(search_param.lower())
            results = {}
            for book in books:
                results[book.id] = book.book_serializer()
            return jsonify({"books": results}), 200
    except AttributeError:
        return jsonify({"msg": "No results found"}), 404


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

            return jsonify(borrow.borrowed_to_dict()), 201

        elif request.method == "POST" and book_status == "borrowed":
            return jsonify({"msg": "Book not available for borrowing"})

        # Return borrowed book by authorised user.
        elif request.method == 'PUT' and book_status == "borrowed":

            try:
                borrowed_book = BorrowedBook.get_borrowed_by_id(book_id)
                borrow_period = str(datetime.now() - (borrowed_book.borrow_date + timedelta(days=10))).split(' ')[0]
                if type(borrow_period) != int:
                    borrow_period = 0

                borrowed_book.update_borrowed(int(borrow_period))
                borrowed_book.save()
                book_details.set_book_status("available")

                return jsonify(borrowed_book.borrowed_to_dict())

            except AttributeError:
                return jsonify({"msg": "cannot return book. Not borrowed by user",
                                "book_status": "borrowed"}), 403

        elif request.method == 'PUT' and book_status == 'available':
            return jsonify({"msg": "Book already available"}), 403

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
        entry = book.borrowed_to_dict().copy()
        entry.update({"book_title": book.book.title})

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
    for entry_log in logs:
        entry = {
            "book_id": entry_log.book_id,
            "timestamp": entry_log.timestamp,
            "action": entry_log.action,
            "success": entry_log.success
            }
        audit_log[entry_log.log_id] = entry

    return jsonify(audit_log), 200
