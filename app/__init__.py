'''app/__init__.py'''

from flask_api import FlaskAPI
from flask import Flask, request, jsonify, session, flash

from config import app_config
from app.models import User, Book

from datetime import datetime, timedelta


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])


    book = Book()
    user = User()

    @app.route('/api/v1/books', methods=['POST'])
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


    @app.route('/api/v1/books/<int:book_id>', methods=['PUT'])
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
                book_details = {"msg":"Book entry not available"}

                response= jsonify(book_details)
                response.status_code = 404

                return response
            
            
    @app.route('/api/v1/books/<int:book_id>', methods=['DELETE'])
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


    @app.route('/api/v1/books', methods=['GET'])
    def retrieve_all_books():
        '''retieves all books in library'''

        if request.method == 'GET':

            library = book.get_all_books()
            response = jsonify(library)

            response.status_code = 200

            return response


    @app.route('/api/v1/books/<int:book_id>', methods=['GET'])
    def get_book(book_id):
        '''gets specific book using book_id'''

        if request.method == 'GET':
            
            try:
                book_details = book.get_book(book_id)

                response = jsonify(book_details)
                response.status_code = 200

                return response

            except KeyError:
                response = jsonify({"msg":"Book not avialable"})
                response.status_code = 404

                return response


    @app.route('/api/v1/users/books/<int:book_id>', methods=['POST'])
    def borrow_return_book(book_id):
        '''allows borrowing/returning of books'''

        if request.method == 'POST':
            data = request.get_json()

            book_info = {}
            try:
                book_details = book.get_book(book_id)
                book_status = book_details["status"]
                if data["acc_status"] == "member" and book_status == "available":
                   
                    book_info = user.set_borrowed( book_status, book_id)
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
                        borrow_period = int(str(current_day - return_day).split(' ')[0])
                        print(current_day, return_day, borrow_period)
                        if borrow_period > 0:
                            borrowed_book["fee_owed"] = borrow_period * 30
                            borrowed_book["borrow_status"] = "unreturned"

                        book.get_book(book_id)["status"] = "returned"
                        response = jsonify(borrowed_book)

                        return response

                    response = jsonify(
                        {"msg": "Book not available for borrowing",
                        "status": "Borrowed"})

                    return response

                elif data["acc_status"] != "member":
                    response = jsonify(
                        {"msg": "Member currently not authorised to borrow book"})

                    return response
                    
            except KeyError:
                response = jsonify({"msg": "Book not avialable"})
                response.status_code = 404

                return response


    @app.route('/api/auth/register', methods=['POST'])
    def create_user_account():
        '''adds new user'''

        if request.method == "POST":

            data = request.get_json()
            user.uid = ['user_id']
            user.name = ['name']
            user.eaddress = data['email']
            user.username = data['username']
            user.password = data['password']
            user.acc_status = data['acc_status']

            if data:
                resp = jsonify({
                    'user_id': user.uid,
                    'name': user.name,
                    'username': user.username,
                    'password': user.password,
                    'acc_status':  user.acc_status,
                }
                )
                user.add_to_reg(user.uid, resp.data)
                #adds new user entry to reister
                resp.status_code = 201

                return resp


    @app.route('/api/auth/login', methods=['POST'])
    def login():
        '''facilitates user login'''

        if request.method == 'POST':

            data = request.get_json()

            user.username = data['username']
            user.password = data['password']

            for account in user.get_all_users():
                if account['username'] == user.username and account['password'] == user.password:
                    session['logged in'] = True
                    flash('Successfully logged in', category='info')


    @app.route('/api/auth/logout', methods=['POST'])
    def logout():
        '''facilitates user logout'''
        if request.method == 'POST':
            session.pop('logged_in', None)
            flash('Successfully logged out', category='info')


    return app
