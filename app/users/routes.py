"""
app/users/routes.py
Holds user/auth API endpoints.
"""

from flask import Flask, Blueprint, request, jsonify, session, flash

from app.users.models import User

users_blueprint = Blueprint('users', __name__)

user = User()


@users_blueprint.route('/register', methods=['POST'])
def create_user_account():
    """
    Adds new user."""

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

            return jsonify(user_details), 201

        else:
            user_details = {"msg": "Username not available. Already in use"}

            return jsonify(user_details), 409


@users_blueprint.route('/login', methods=['POST'])
def login():
    """
    Facilitates user login."""

    if request.method == 'POST':

        data = request.get_json()

        try:
            user_details = user.get_user(data['username'])
            if user_details['password'] == data['password']:
                session['username'] = data['username']
                session['logged_in'] = True
                flash('Successfully logged in', category='info')

                return jsonify({"message" : "Successfully logged in"})

            else:
                return jsonify({"message" : "Incorrect password"})

        except KeyError:
            return jsonify({"message" : "Account not available"})
 

@users_blueprint.route('/logout', methods=['POST'])
def logout():
    """
    Facilitates user logout."""

    if request.method == 'POST' and session['logged_in']:
        session.pop('username', None)
        session.pop('logged_in', None)
        flash('Successfully logged out', category='info')

        return jsonify({"message" : "Successfully logged out"})


@users_blueprint.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Resets user password."""

    if request.method == 'POST' and session['logged_in']:
        
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

            return jsonify({"message" : "Successfully changed password"}), 202

        else:
            return jsonify({"message" : "Current password incorrect"})
