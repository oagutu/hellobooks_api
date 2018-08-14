"""
app/users/routes.py
Holds user/auth API endpoints.
"""

from flask import Blueprint, request, jsonify, flash
from flask_jwt_extended import (
    jwt_required, create_access_token, get_raw_jwt, get_jwt_identity, jwt_optional
)
from passlib.hash import sha256_crypt


from app.users.models import User, UserLog
from app.blacklist.models import Blacklist
from app.helpers import already_logged_in, verify_user_info, log
from app.blacklist.helpers import admin_required

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/register', methods=['POST'])
def create_user_account():
    """
    Adds new user.

    :return: created user details or failure message
    :rtype: json obj
    """

    data = request.get_json()

    invalid_msg = verify_user_info(data, True)
    if invalid_msg == 'Email address already in use':
        return jsonify({"msg": invalid_msg}), 409
    elif invalid_msg:
        return jsonify({"msg": invalid_msg}), 400

    user_info = dict()
    for val in ('name', 'email', 'username', 'password', 'user_id', 'acc_status'):
        if val in data:
            user_info[val] = data[val]

    if not User.get_user(data['username']):
        user = User(user_info)
        user.add_to_reg()

        log(user, 'INSERT')
        msg = "Successfully registered {}" .format(data['username'])

        return jsonify({"msg": msg}), 201

    else:
        return jsonify({"msg": "Username not available. Already in use"}), 409


@users_blueprint.route('/login', methods=['POST'])
@jwt_optional
@already_logged_in
def login():
    """
    Facilitate user login.

    :return: login message
    :rtype: json obj
    """

    data = request.get_json()

    invalid_msg = verify_user_info(data, False)
    if invalid_msg:
        return jsonify({"msg": invalid_msg}), 400

    try:
        isverified = User.verify_pass(data['username'], data['password'])

        if isverified:
            user_details = User.get_user(data['username'])
            access_token = create_access_token(identity=user_details)

            message = "Successfully logged in as: " + data['username']

            response = jsonify({
                "role": user_details.acc_status,
                "msg": message,
                "access_token": access_token}
            )

            response.headers['Authorization'] = access_token
            response.status_code = 200

            return response

        else:
            return jsonify({"msg": "Incorrect password"}), 401

    except (KeyError, AttributeError):
        return jsonify({"msg": "Account not available"})


@users_blueprint.route('/logout', methods=['POST'])
@jwt_required
def logout():
    """
    Facilitate user logout.

    :return: logout message
    :rtype: json obj
    """

    token_index = get_raw_jwt()['jti']
    Blacklist.add_to_blacklist(Blacklist(token_index))

    return jsonify({"message": "Successfully logged out"})


@users_blueprint.route('/reset-password', methods=['POST'])
@jwt_required
def reset_password():
    """
    Reset user password.

    :return: password reset message
    :rtype: json obj
    """

    data = request.get_json()
    user_info = [
        get_jwt_identity(),
        data['current_password'],
        data['new_password']
    ]

    user_details = User.get_user(get_jwt_identity())

    if sha256_crypt.verify(user_info[1], user_details.password) and not \
            User.verify_pass(user_info[0], user_info[2]):
        user_details.set_password(user_info)

        log(user_details, 'pipUPDATE')

        flash('Successfully changed password', category='info')

        return jsonify({"message": "Successfully changed password"}), 200

    elif sha256_crypt.verify(user_info[1], user_details.password) and \
            User.verify_pass(user_info[0], user_info[2]):
        return jsonify({"message": "New password cannot be the same as old password"})
    else:
        return jsonify({"message": "Current password incorrect"})


@users_blueprint.route('/users/status_change', methods=['POST'])
@jwt_required
@admin_required
def update_user_status():
    """
    Update user status.

    :return: update user status message
    :rtype: json obj
    """

    data = request.get_json()
    status_options = ['banned', 'suspended', 'admin', 'member']

    if 'new_status' not in data or data['new_status'] not in status_options:
        return jsonify({"msg": "Invalid status option"}), 400

    if 'user' not in data:
        return jsonify({"msg": "Missing user_id/username"}), 400
    else:
        user_param = data['user']

    if not User.get_user(user_param):
        return jsonify({"msg": "User does NOT exist. Invalid Username/UserID."}), 400

    user = User.get_user(user_param)
    user.change_status(data['new_status'])

    return jsonify({'msg': '{0} changed to {1}'.format(data['user'], data['new_status'])}), 200


@users_blueprint.route('/users', methods=['GET'])
@jwt_required
@admin_required
def get_users():
    """Get all users"""

    users = User.get_all_users()
    members = []

    for user in users:
        entry = user.user_serializer()
        members.append(entry)

    return jsonify(members), 200


@users_blueprint.route('/users/logs', methods=['GET'])
@jwt_required
@admin_required
def get_log():
    """
    Retrieve user logs

    :return: user logs
    :rtype: json obj
    """

    user_id = request.args.get("user_id")

    if user_id:
        logs = UserLog.get_logs(int(user_id))
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
