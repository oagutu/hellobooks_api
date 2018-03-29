'''app/__init__.py'''

from flask_api import FlaskAPI
from flask import Flask, request, jsonify, session, flash

from config import app_config
from . import models


value_list = ['bk_id', 'title', 'code', 'author', 'synopsis'
              'genre', 'sub_genre', 'status']

book = models.Book()
user = models.User()

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    @app.route('/api/books', methods=['POST'])
    def add_book():
        '''adds specified book to library'''

        if request.method == "POST":
            data = request.get_json()
            book_id = data['book_id']
            title = data['title']
            author = data['author']

            book_details = book.set_book(book_id, title, author)
            #returns dictionary with book details

            response = jsonify(book_details)

            return response

        

    # @app.route('/api/books', methods=['POST'])
    # def add_book():
    #     '''adds book to library'''

    #     if request.method == "POST":

    #         data = request.get_json()
            
    #         book.bk_id = data['bk_id']
    #         book.title = data['title']
    #         book.code = data['code']
    #         book.author = data['author']
    #         book.synopsis = data['synopsis']
    #         book.genre = data['genre']
    #         book.sub_genre = data['sub_genre']
    #         book.status = data['status']

    #         if data:
    #             resp = jsonify({
    #                 'bk_id': book.bk_id,
    #                 'title': book.title,
    #                 'code': book.code,
    #                 'author': book.author,
    #                 'synopsis': book.synopsis,
    #                 'genre': book.genre,
    #                 'sub_genre': book.sub_genre,
    #                 'status': book.status
    #             }
    #             )
    #             book.add_to_lib(book.bk_id, resp.data)
    #             #adds new book entry to lib
    #             resp.status_code = 201

    #             return resp


    @app.route('/api/books/<int:bk_id>', methods=['PUT'])
    def update_book():

        if request.method == "PUT":

            data = request.get_json()
            temp_data = {}

            for val in value_list:
                if data.get(val) in data:
                    book.val = data[val]
                    temp_data[val] = book.val
            resp = jsonify(temp_data)

            return resp


    @app.route('/api/books/<int:bk_id>', methods=['DELETE'])
    def remove_book(bk_id):

        if request.method == 'DELETE':
            data = request.get_json()
            book.bk_id = data['bk_id']
            del book.library[book.bk_id]

            resp = jsonify({'bk_id': book.bk_id,
                            'title': book.title, })

            resp.msg = 'Book entry deleted'

            return resp


    @app.route('/api/books', methods=['GET'])
    def retrieve_all_books():
        '''retieves all books in library'''

        if request.method == 'GET':

            for indv_book in book.get_all_books():
                resp = jsonify(indv_book)
            resp.status_code = 200

            return resp


    @app.route('/api/books/<int:bk_id>', methods=['GET'])
    def get_book(bk_id):
        '''gets specific book'''

        if request.method == 'GET':

            for bk in book.get_all_books():
                if bk['bk_id'] == bk_id:
                    resp = jsonify(bk)

                    resp.status_code = 200

                    return resp



    @app.route('/api/users/books/<int:id>', methods=['POST'])
    def borrow_return_book(bk_id):
        '''allows borrowing/returning of books'''

        if request.method == 'POST':
            data = request.get_json(force=True)
            book.book_id = data['bk_id']

            for bk in book.get_all_books():
                if bk['bk_id'] == book.book_id and bk['status'] == 'available':
                    bk['status'] = 'borrowed'
                    resp = jsonify(bk)

                    return resp

                bk['status'] = 'returned'
                resp = jsonify(bk)

                return resp


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
            user.acc_type = data['acc_type']

            if data:
                resp = jsonify({
                    'user_id': user.uid,
                    'name': user.name,
                    'username': user.username,
                    'password': user.password,
                    'acc_type':  user.acc_type,
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
