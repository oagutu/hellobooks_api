"""
    tests/test_books/test_create_user.py
    Provides testing for book endpoints.
"""

import unittest
from tests.test_users.test_users import UserEndpointsTestCase


class CreateUserTestCase(UserEndpointsTestCase):
    """Test user API endpoints"""

    def test_create_user_account(self):
        """
        Tests create_user_account functionality."""

        result = self.user(self.user_details)
        self.assertEqual(result.status_code, 201)
        self.assertIn(b'JD', result.data)
        self.assertIn(b'Jane Doe', result.data)

    def test_create_user_account_with_conflict(self):
        """Test if username already in use when creating an account."""

        data = {
                "name": "John Doe",
                "username": "Doe",
                "password": "qwerty",
                "email": "another@test.com",
        }
        result = self.user(data)
        self.assertEqual(result.status_code, 409)
        self.assertIn(b'Username not available. Already in use', result.data)

    def test_create_user_account_with_invalid_pass(self):
        """Test if password incorrect."""

        data = {
                "name": "mary",
                "user_id": "44",
                "username": "m",
                "password": "",
                "email": "gmail@mary.com"
        }
        result = self.user(data)
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'Invalid Password', result.data)

    def test_create_user_account_with_invalid_username(self):
        """Test if username incorrect."""

        data = {
                "name": "mary",
                "user_id": "44",
                "username": "",
                "password": "123",
                "email": "gmail@mary.com"}
        result = self.user(data)
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'Invalid Username', result.data)

    def test_create_user_account_with_invalid_email(self):
        """Test if email incorrect."""

        data = {
                "name": "mary",
                "user_id": "44",
                "username": "m",
                "password": "123",
                "email": "gmaimary.com"}
        result = self.user(data)
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'Invalid Email', result.data)

    def test_create_user_account_with_email_conflict(self):
        """Test if email already in use."""

        data = {
                "name": "mary",
                "user_id": "44",
                "username": "m",
                "password": "123",
                "email": "gmail@mary.com"}
        self.assertEqual(self.user(data).status_code, 201)

        data = {
            "name": "mary",
            "user_id": "44",
            "username": "m",
            "password": "123",
            "email": "gmail@mary.com"}
        result = self.user(data)
        self.assertEqual(result.status_code, 409)
        self.assertIn(b'Email address already in use', result.data)

    def test_create_user_acc_no_email(self):
        """Test if no email provided."""

        data = {
                "name": "mary",
                "user_id": "44",
                "username": "m",
                "password": "123"}
        result = self.user(data)

        self.assertEqual(result.status_code, 400)
        self.assertIn(b'No email provided', result.data)


if __name__ == '__main__':
    unittest.main()
