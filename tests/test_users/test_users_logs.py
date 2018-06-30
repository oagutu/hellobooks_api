"""
    tests/test_users/test_user_logs.py
    Provides testing for user logs endpoints.
"""

import unittest
import json
from tests.test_users.test_users import UserEndpointsTestCase


class UserLogsTestCase(UserEndpointsTestCase):
    """Test user API endpoints"""

    def test_logout(self):
        """Test logout"""

        result = self.client.post(
            'api/v1/auth/logout',
            headers={'Authorization': 'Bearer {}'.format(self.tokens['test_token'])})
        self.assertIn(b'Successfully logged out', result.data)

    def test_get_add_user_log(self):
        """Test if user data creation logged."""

        result = self.client.get(
            '/api/v1/auth/users/logs?user_id=654321',
            headers={
                'Authorization': 'Bearer {}'.format(self.tokens["test_token"])})
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'INSERT', result.data)

    def test_get_add_user_log_unauthorised_user(self):
        """Test that unauthorised user cannot access user logs."""

        self.user(self.user_details)
        result = self.user({'username': 'JD', 'password': 'qwerty'}, False)
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
