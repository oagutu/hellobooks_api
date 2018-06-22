"""
    tests/test_users.py
    Provides testing for book endpoints.
"""

import unittest
import json

from app import create_app, db


class UserEndpointsTestCase(unittest.TestCase):
    """Test user API endpoints."""

    def setUp(self):
        """et up testing environment variables."""

        self.app = create_app('testing')
        self.client = self.app.test_client()

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

        self.user_details = {
            "name": "Jane Doe",
            "user_id": 123456,
            "username": "JD",
            "password": "qwerty",
            "email": "abc@gfg.com",
            "acc_status": "member",
            "borrowed_books": {}
        }

        self.user_details_two = {
            "name": "Baba",
            "user_id": 1234,
            "username": "John",
            "password": "qwerty",
            "email": "qwerty@keyboard.com",
            "acc_status": "suspended",
            "borrowed_books": {}}

        self.user_details_four = {
            "name": "John Doe",
            "user_id": 654321,
            "username": "Doe",
            "password": "qwerty",
            "email": "abc@test.com",
            "acc_status": "admin",
            "borrowed_books": {}
        }

        self.tokens = {}

        self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details_four),
            headers={"content-type": "application/json"})

        res = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'Doe', 'password': 'qwerty'}),
            headers={"content-type": "application/json"})
        self.tokens['test_token'] = res.headers['Authorization']

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def test_create_user_account(self):
        """
        Tests create_user_account functionality."""

        result = self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details),
            headers={"content-type": "application/json"})
        # print(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertIn(b'JD', result.data)
        self.assertIn(b'Jane Doe', result.data)

    def test_create_user_account_with_conflict(self):
        """Test if username already in use when creating an account."""

        result = self.client.post(
            "/api/v1/auth/register",
            data=json.dumps({
                "name": "John Doe",
                "username": "Doe",
                "password": "qwerty",
                "email": "another@test.com",
                }
            ),
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 409)
        self.assertIn(b'Username not available. Already in use', result.data)

    def test_create_user_account_with_invalid_pass(self):
        """Test if password incorrect."""

        result = self.client.post(
            "/api/v1/auth/register",
            data=json.dumps({
                "name": "mary",
                "user_id": "44",
                "username": "m",
                "password": "",
                "email": "gmail@mary.com"}),
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'Invalid Password', result.data)

    def test_create_user_account_with_invalid_username(self):
        """Test if username incorrect."""

        result = self.client.post(
            "/api/v1/auth/register",
            data=json.dumps({
                "name": "mary",
                "user_id": "44",
                "username": "",
                "password": "123",
                "email": "gmail@mary.com"}),
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'Invalid Username', result.data)

    def test_create_user_account_with_invalid_email(self):
        """Test if email incorrect."""

        result = self.client.post(
            "/api/v1/auth/register",
            data=json.dumps({
                "name": "mary",
                "user_id": "44",
                "username": "m",
                "password": "123",
                "email": "gmaimary.com"}),
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'Invalid Email', result.data)

    def test_create_user_account_with_email_conflict(self):
        """Test if email already in use."""

        self.assertEqual(self.client.post(
            "/api/v1/auth/register",
            data=json.dumps({
                "name": "mary",
                "user_id": "44",
                "username": "m",
                "password": "123",
                "email": "gmail@mary.com"}),
            headers={"content-type": "application/json"}).status_code, 201)

        result = self.client.post(
            "/api/v1/auth/register",
            data=json.dumps({
                "name": "mary",
                "username": "mmm",
                "password": "123",
                "email": "gmail@mary.com"}),
            headers={"content-type": "application/json"})

        self.assertEqual(result.status_code, 409)
        self.assertIn(b'Email address already in use', result.data)

    def test_crete_user_acc_no_email(self):
        """Test if no email provided."""

        result = self.client.post(
            "/api/v1/auth/register",
            data=json.dumps({
                "name": "mary",
                "user_id": "44",
                "username": "m",
                "password": "123"}),
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'No email provided', result.data)

    def test_login(self):
        """Test login() functionality."""

        self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details),
            headers={"content-type": "application/json"})

        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'JD', 'password': 'qwerty'}),
            headers={"content-type": "application/json"})
        token = result.headers['Authorization']
        self.tokens['John'] = token
        self.assertIn(b'Successfully logged in', result.data)

    def login_invalid_username(self):
        """Test login with invalid/missing password"""

        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': '', 'password': 'qwerty'}),
            headers={"content-type": "application/json"})
        self.assertIn(b'Invalid/Missing Username', result.data)

    def test_login_invalid_password(self):
        """Test login with invalid/missing password"""

        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'Doe', 'password': ''}),
            headers={"content-type": "application/json"})
        self.assertIn(b'Invalid/Missing Password', result.data)

    def test_login_incorrect_password(self):
        """Test login with wrong password."""

        self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details),
            headers={"content-type": "application/json"})

        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'JD', 'password': 'rose'}),
            headers={"content-type": "application/json"})
        self.assertIn(b'Incorrect password', result.data)

    def test_login_incorrect_username(self):
        """Test login with wrong username."""
        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'Amber', 'password': 'rose'}),
            headers={"content-type": "application/json"})
        self.assertIn(b'Account not available', result.data)

    def test_reset_password(self):
        """Test password reset."""

        result = self.client.post(
            'api/v1/auth/reset-password',
            data=json.dumps({'current_password': 'qwerty', 'new_password': '09876'}),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["test_token"])})
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Successfully changed password', result.data)

    def test_reset_password_incorrect_current_password(self):
        """Test password reset with incorrect current password."""
        
        result = self.client.post(
            'api/v1/auth/reset-password',
            data=json.dumps({'username': 'JD', 'current_password': 'pass123', 'new_password': '09876'}),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens['test_token'])})
        self.assertIn(b'Current password incorrect', result.data)

    def test_logout(self):
        """Test logout"""

        result = self.client.post(
            'api/v1/auth/logout',
            headers={'Authorization': 'Bearer {}' .format(self.tokens['test_token'])}
        )
        self.assertIn(b'Successfully logged out', result.data)

    def test_user_status_change(self):
        """Test if admin able to change user status."""

        self.assertEqual(self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details_two),
            headers={"content-type": "application/json"}).status_code, 201)

        result = self.client.post(
            '/api/v1/auth/users/status_change',
            data=json.dumps({'user': 1234, 'new_status': 'banned'}),
            headers={
                'content-type': 'application/json',
                'Authorization': 'Bearer {}'.format(self.tokens["test_token"])})
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'banned', result.data)

    def test_user_status_change_missing_user_info(self):
        """Test if admin able to change user status without giving user."""

        self.assertEqual(self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details_two),
            headers={"content-type": "application/json"}).status_code, 201)

        result = self.client.post(
            '/api/v1/auth/users/status_change',
            data=json.dumps({'new_status': 'banned'}),
            headers={
                'content-type': 'application/json',
                'Authorization': 'Bearer {}'.format(self.tokens["test_token"])})
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'Missing user_id/username', result.data)

    def test_user_status_change_invalid_status(self):
        """Test if admin able to change user status with invalid status option."""

        self.assertEqual(self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details_two),
            headers={"content-type": "application/json"}).status_code, 201)

        result = self.client.post(
            '/api/v1/auth/users/status_change',
            data=json.dumps({'new_status': 'valid'}),
            headers={
                'content-type': 'application/json',
                'Authorization': 'Bearer {}'.format(self.tokens["test_token"])})
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'Invalid status option', result.data)

    def test_user_status_change_missing_user(self):
        """Test if admin able to change user status for nonexistent user."""

        result = self.client.post(
            '/api/v1/auth/users/status_change',
            data=json.dumps({'user': 'nonexistent', 'new_status': 'banned'}),
            headers={
                'content-type': 'application/json',
                'Authorization': 'Bearer {}'.format(self.tokens["test_token"])})
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'User does NOT exist. Invalid Username/UserID.', result.data)

    def test_user_status_change_invalid_method(self):
        """Test if admin able to change user status for invalid method."""

        result = self.client.put(
            '/api/v1/auth/users/status_change',
            data=json.dumps({'user': 1234, 'new_status': 'banned'}),
            headers={
                'content-type': 'application/json',
                'Authorization': 'Bearer {}'.format(self.tokens["test_token"])})
        self.assertEqual(result.status_code, 405)

    def test_user_status_change_by_unauthorised_user(self):
        """Test if non-admin able to change user status."""

        self.assertEqual(self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details_two),
            headers={"content-type": "application/json"}).status_code, 201)

        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'John', 'password': 'qwerty'}),
            headers={"content-type": "application/json"})
        self.assertIn(b'Successfully logged in', result.data)
        token = result.headers['Authorization']

        result = self.client.put(
            '/api/v1/auth/users/status_change',
            data=json.dumps({'user': 1234, 'new_status': 'banned'}),
            headers={
                'content-type': 'application/json',
                'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(result.status_code, 405)

    def test_get_add_user_log(self):
        """Test if user data creation logged."""

        result = self.client.get(
            '/api/v1/auth/users/logs?user_id=654321',
            headers={
                'Authorization': 'Bearer {}'.format(self.tokens["test_token"])})
        print(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'INSERT', result.data)

    def test_get_add_user_log_unauthorised_user(self):
        """Test that unauthorised user cannot access user logs."""

        self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details),
            headers={"content-type": "application/json"})

        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'JD', 'password': 'qwerty'}),
            headers={"content-type": "application/json"})
        token = result.headers['Authorization']

        result = self.client.get(
            '/api/v1/auth/users/logs',
            headers={
                'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(result.status_code, 403)
        self.assertIn(b'Unauthorised User', result.data)

    def test_get_reset_password_log(self):
        """Test getting log of reset user password."""

        self.assertEqual(self.client.post(
            'api/v1/auth/reset-password',
            data=json.dumps({'current_password': 'qwerty', 'new_password': '09876'}),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["test_token"])}).status_code, 200)

        result = self.client.get(
            '/api/v1/auth/users/logs',
            headers={
                'Authorization': 'Bearer {}'.format(self.tokens["test_token"])})
        self.assertIn(b'UPDATE', result.data)


if __name__ == '__main__':
    unittest.main()
