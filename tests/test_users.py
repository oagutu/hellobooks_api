"""
    tests/test_users.py
    Provides testing for book endpoints.
"""

import unittest
import json

from app import create_app, db


class UserEndpointsTestCase(unittest.TestCase):
    """
    Tests user API endpoints."""

    def setUp(self):
        """
        Sets up testing environment variables"""

        self.app = create_app('development')
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
            "name": "Baba'",
            "user_id": "1234",
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

        self.user_details_three = {
            "name": "one",
            "user_id": "",
            "username": "m",
            "password": "",
            "email": ""
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
        """
        Tests if username already in use when creating an account"""

        result = self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details_four),
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 409)
        self.assertIn(b'Username not available. Already in use', result.data)

    def test_create_user_account_with_invalid_pass(self):
        """
        Tests if password incorrect"""

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
        """
        Tests if username incorrect"""

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
        """
        Tests if email incorrect"""

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

    def test_crete_user_acc_no_email(self):
        """
        Tests if no email provided"""

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
        """
        Tests login() functionality."""

        self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details),
            headers={"content-type": "application/json"})

        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'JD', 'password': 'qwerty'}),
            headers={"content-type": "application/json"})
        token = result.headers['Authorization']
        print(token)
        self.tokens['John'] = token
        self.assertIn(b'Successfully logged in', result.data)

    def test_login_incorrect_pasword(self):
        """
        Tests login with wrong password"""

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
        """
        Tests login with wrong username."""
        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'Amber', 'password': 'rose'}),
            headers={"content-type": "application/json"})
        self.assertIn(b'Account not available', result.data)

    def test_reset_password(self):
        """
        Tests password reset."""

        result = self.client.post(
            'api/v1/auth/reset-password',
            data=json.dumps({'current_password': 'qwerty', 'new_password': '09876'}),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["test_token"])})
        self.assertEqual(result.status_code, 202)
        self.assertIn(b'Successfully changed password', result.data)

    def test_reset_password_incorrect_current_password(self):
        """
        Tests password reset with incorrect current password."""
        
        result = self.client.post(
            'api/v1/auth/reset-password',
            data=json.dumps({'username': 'JD', 'current_password': 'pass123', 'new_password': '09876'}),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens['test_token'])})
        self.assertIn(b'Current password incorrect', result.data)

    def test_logout(self):
        """
        Tests logout"""

        result = self.client.post(
            'api/v1/auth/logout',
            headers={'Authorization': 'Bearer {}' .format(self.tokens['test_token'])}
        )
        self.assertIn(b'Successfully logged out', result.data)

    # def test_user_status_change(self):
    #     """
    #     Test if admin able to change user status"""
    #
    #     result = self.client.post(
    #         '/api/v1/auth/users/',
    #         headers={
    #             'Authorization': 'Bearer {}'.format(self.tokens["test_token"])})
    #     self.assertEqual(result.status_code, 200)

    def test_get_add_user_log(self):
        """
        Test if user data creation logged."""

        result = self.client.get(
            '/api/v1/auth/users/logs',
            headers={
                'Authorization': 'Bearer {}'.format(self.tokens["test_token"])})
        print(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'INSERT', result.data)

    def test_get_add_user_log_unauthorised_user(self):
        """
        Test if user data creation logged by unauthorised user."""

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
        self.assertEqual(result.status_code, 401)
        self.assertIn(b'User not authorised', result.data)

    def test_get_reset_password_log(self):
        """
        Test getting log of reset user password"""

        self.assertEqual(self.client.post(
            'api/v1/auth/reset-password',
            data=json.dumps({'current_password': 'qwerty', 'new_password': '09876'}),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["test_token"])}).status_code, 202)

        result = self.client.get(
            '/api/v1/auth/users/logs',
            headers={
                'Authorization': 'Bearer {}'.format(self.tokens["test_token"])})
        print(result.data)
        self.assertIn(b'UPDATE', result.data)


if __name__ == '__main__':
    unittest.main()
