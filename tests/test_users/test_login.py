"""
    tests/test_users/test_login.py
    Provides testing for login endpoints.
"""

import unittest
from tests.test_users.test_users import UserEndpointsTestCase


class LoginTestCase(UserEndpointsTestCase):
    """Test user API endpoints"""

    def test_login(self):
        """Test login() functionality."""

        self.user(self.user_details)
        result = self.user({'username': 'JD', 'password': 'qwerty'}, False)
        token = result.headers['Authorization']
        self.tokens['John'] = token
        self.assertIn(b'Successfully logged in', result.data)

    def login_invalid_username(self):
        """Test login with invalid/missing password"""

        result = self.user({'username': '', 'password': 'qwerty'}, False)
        self.assertIn(b'Invalid/Missing Username', result.data)

    def test_login_invalid_password(self):
        """Test login with invalid/missing password"""

        result = self.user({'username': 'Doe', 'password': ''}, False)
        self.assertIn(b'Invalid/Missing Password', result.data)

    def test_login_incorrect_password(self):
        """Test login with wrong password."""

        self.user(self.user_details)
        result = self.user({'username': 'JD', 'password': 'rose'}, False)
        self.assertIn(b'Incorrect password', result.data)

    def test_login_incorrect_username(self):
        """Test login with wrong username."""

        result = self.user({'username': 'Amber', 'password': 'rose'}, False)
        self.assertIn(b'Account not available', result.data)


if __name__ == '__main__':
    unittest.main()
