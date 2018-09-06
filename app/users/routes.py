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

    user_info['username'] = user_info['username'].lower()
    if not User.get_user(data['username'].lower()):
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
                "access_token": access_token,
                "user": user_details.email},
            )

            response.headers['Authorization'] = access_token
            response.status_code = 200

            return response

        else:
            return jsonify({"msg": "Incorrect password"}), 401

    except (KeyError, AttributeError) as e:
        print(e)
        return jsonify({"msg": "Account not available"}), 404


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
        data['new_password'],
        data['confirm_password']
    ]

    if data['new_password'] != data['confirm_password']:
        return jsonify({"message": "invalid confirm password input"}), 400

    user_details = User.get_user(get_jwt_identity())

    if sha256_crypt.verify(user_info[1], user_details.password) and not \
            User.verify_pass(user_info[0], user_info[2]):
        user_details.set_password(user_info)

        log(user_details, 'UPDATE')

        flash('Successfully changed password', category='info')

        return jsonify({"message": "Successfully changed password"}), 200

    elif sha256_crypt.verify(user_info[1], user_details.password) and \
            User.verify_pass(user_info[0], user_info[2]):
        return jsonify({"message": "New password cannot be the same as old password"}), 400
    else:
        return jsonify({"message": "Current password incorrect"}), 403


@users_blueprint.route('/users/status_change', methods=['POST'])
@jwt_required
@admin_required
def update_user_status():
    """
    Update user status.

    :return: update user status message
    :rtype: json obj
    """

    data = request.get_json(force=True)
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
        del entry['books']
        members.append(entry)

    return jsonify(members), 200


@users_blueprint.route('/users/profile', methods=['GET'])
@jwt_required
def get_user():
    """Get single user"""

    user_param = request.args.get("q")
    user = User.get_user(user_param)
    user = user.user_serializer()
    del user['books']
    user_result = {'user_data': user, 'msg': f'User {user_param} successfully found'}

    return jsonify(user_result), 200


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

    audit_log = []
    for entry_log in logs:
        audit_log.append({
            "log_id": entry_log.log_id,
            "user_id": entry_log.user_id,
            "timestamp": entry_log.timestamp,
            "action": entry_log.action,
            "success": entry_log.success
            })
    audit_log = {'logs': audit_log, 'count': len(audit_log)}

    return jsonify(audit_log), 200
