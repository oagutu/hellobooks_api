"""
app/users/routes.py
Holds user/auth API endpoints.
"""

from flask import Blueprint, request, jsonify, session, flash
from flask_jwt_extended import (
    jwt_required, create_access_token, get_raw_jwt
)

from app.users.models import User

users_blueprint = Blueprint('users', __name__)

user = User()
blacklist = set()


@users_blueprint.route('/register', methods=['POST'])
def create_user_account():
    """
    Adds new user."""

    if request.method == "POST":

        data = request.get_json()

        user_info = {
            "user_id": data['user_id'],
            "name": data['name'],
            "email": data['email'],
            "username": data['username'],
            "password": data['password'],
            "acc_status": data['acc_status'],
            "borrowed_books": data['borrowed_books']
        }

        if data['username'] not in user.get_register():
            user_details = user.set_user(user_info)
            # Returns dictionary with book details.

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
                access_token = create_access_token(identity=data['username'])

                response = jsonify({
                    "message": "Successfully logged in",
                    "access_token": access_token}
                )

                response.headers['Authorization'] = access_token

                return response

            else:
                return jsonify({"message": "Incorrect password"})

        except KeyError:
            return jsonify({"message": "Account not available"})
 

@users_blueprint.route('/logout', methods=['POST'])
@jwt_required
def logout():
    """
    Facilitates user logout."""

    if request.method == 'POST':
        blacklist.add(get_raw_jwt()['jti'])

        return jsonify({"message": "Successfully logged out"})


@users_blueprint.route('/reset-password', methods=['POST'])
@jwt_required
def reset_password():
    """
    Resets user password."""

    if request.method == 'POST':
        
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

            return jsonify({"message": "Successfully changed password"}), 202

        else:
            return jsonify({"message": "Current password incorrect"})
