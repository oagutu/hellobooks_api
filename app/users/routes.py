'''
    app/users/routes.py
    Holds user/auth API endpoints
'''
from flask import Flask, Blueprint, request, jsonify, session, flash

from app.models import User

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/index/')
def index():
    return "<h1>Hello World</h1>"


user = User()

@users_blueprint.route('/register', methods=['POST'])
def create_user_account():
    '''adds new user'''

    if request.method == "POST":

        data = request.get_json()

        user_info = [
            data['user_id'],
            data['name'],
            data['email'],
            data['username'],
            data['password'],
            data['acc_status'],
            data['borrowed_books']
        ]

        if data['username'] not in user.get_register():
            user_details = user.set_user(user_info)
            #returns dictionary with book details

            response = jsonify(user_details)

            response.status_code = 201

            return response
        else:
            book_details = {"msg": "User ID not available. Already in use"}

            response = jsonify(book_details)
            response.status_code = 404

            return response

@users_blueprint.route('/login', methods=['POST'])
def login():
    '''facilitates user login'''

    if request.method == 'POST':

        data = request.get_json()

        try:
            user_details = user.get_user(data['username'])
            if user_details['password'] == data['password']:
                session['username'] = data['username']
                session['logged_in'] = True
                flash('Successfully logged in', category='info')

                response = jsonify({"message": "Successfully logged in"})
                return response

            else:
                reponse = jsonify({"message": "Incorrect password"})

                return reponse

        except KeyError:
            reponse = jsonify({"message": "Account not available"})

            return reponse
            

@users_blueprint.route('/logout', methods=['POST'])
def logout():
    '''facilitates user logout'''
    if request.method == 'POST' and session['logged_in'] == True:
        session.pop('username', None)
        session.pop('logged_in', None)
        flash('Successfully logged out', category='info')

        response = jsonify({"message": "Successfully logged out"})
        return response


@users_blueprint.route('/reset-password', methods=['POST'])
def reset_password():
    '''resets user password'''
    if request.method == 'POST' and session['logged_in'] == True:
        
        data = request.get_json()
        user_info = [
            data['username'],
            data['current_password'],
            data['new_password']
        ]

        user_details = user.get_user(data['username'])
        if user_details['password'] == data['current_password']:
            user.set_password(user_info)
            flash('Successfully changed password', category='info')

            response = jsonify({"message": "Successfully changed password"})
            return response
        else:
            response = jsonify({"message": "Current password incorrect"})
            return response
        
