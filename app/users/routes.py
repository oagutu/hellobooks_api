"""
app/users/routes.py
Holds user/auth API endpoints.
"""

from flask import Blueprint, request, jsonify, flash
from flask_jwt_extended import (
    jwt_required, create_access_token, get_raw_jwt, get_jwt_identity
)
import re

from app.users.models import User, UserLog

users_blueprint = Blueprint('users', __name__)

blacklist = set()


@users_blueprint.route('/register', methods=['POST'])
def create_user_account():
    """
    Adds new user."""

    if request.method == "POST":

        data = request.get_json()

        if len(data['password'].strip()) < 1 or 'password' not in data:
            return jsonify({"msg": "Invalid Password"}), 400

        if len(data['username'].strip()) < 1 or 'username' not in data:
            return jsonify({"msg": "Invalid Username"}), 400

        try:
            email = data['email'].lower()
            pattern = r"^[a-z0-9]+(\.*-*[a-z0-9]*)*@[a-z0-9]+(\.*-*[a-z0-9]*)*(\.[a-z0-9]+)+$"
            match = re.search(pattern, email)
            if not match:
                return jsonify({"msg": "Invalid Email"}), 400
        except KeyError:
            return jsonify({"msg": "No email provided"}), 400

        user_info = {
            "name": data['name'],
            "email": email,
            "username": data['username'],
            "password": data['password']
        }

        if 'acc_status' in data:
            user_info['acc_status'] = data['acc_status']
        if 'borrowed_books' in data and len(data['borrowed_books']) > 0:
            user_info["borrowed_books"] = data["borrowed_books"]
        # print(user_info)

        if not User.get_user(data['username']):
            user = User(user_info)
            # print(user)
            user.add_to_reg()

            if not user.id:
                UserLog(user.id, action='INSERT').add_to_log()
            else:
                UserLog(user.id, action='INSERT', success=False).add_to_log()

            return jsonify({
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "username": user.username,
                "password": user.password,
                "account_status": user.acc_status
            }), 201

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
            user_details = User.get_user(data['username'])
            if user_details.password == data['password']:
                access_token = create_access_token(identity=data['username'])

                response = jsonify({
                    "message": "Successfully logged in",
                    "access_token": access_token}
                )

                response.headers['Authorization'] = access_token

                return response

            else:
                return jsonify({"message": "Incorrect password"})

        except (KeyError, AttributeError):
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
            get_jwt_identity(),
            data['current_password'],
            data['new_password']
        ]

        user_details = User.get_user(get_jwt_identity())
        if user_details.password == data['current_password']:
            user_details.set_password(user_info)

            if user_details.id:
                UserLog(user_details.id, action='UPDATE').add_to_log()
            else:
                UserLog(user_details.id, action='UPDATE', success=False).add_to_log()

            flash('Successfully changed password', category='info')

            return jsonify({"message": "Successfully changed password"}), 202

        else:
            return jsonify({"message": "Current password incorrect"})


@users_blueprint.route('/users/logs', methods=['GET'])
@jwt_required
def get_log():
    """
    Enables viewing of book logs."""

    acc_type = User.get_user(get_jwt_identity())
    book_id = request.args.get("user_id")

    if request.method == 'GET' and acc_type.acc_status == "admin":
        if book_id:
            logs = UserLog.get_logs(book_id)
        else:
            logs = UserLog.get_logs()

        audit_log = {}
        for log in logs:
            entry = {
                "user_id": log.user_id,
                "timestamp": log.timestamp,
                "action": log.action,
                "success": log.success
                }
            audit_log[log.log_id] = entry

        return jsonify(audit_log), 200
    else:
        return jsonify({'msg': 'User not authorised'}), 401
