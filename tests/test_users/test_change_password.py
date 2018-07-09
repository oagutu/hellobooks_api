"""
    tests/test_users/test_change_password.py
    Provides testing for password change endpoints.
"""

import unittest
import json
from tests.test_users.test_users import UserEndpointsTestCase


class ChangePassTestCase(UserEndpointsTestCase):
    """Test user API endpoints"""

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


if __name__ == '__main__':
    unittest.main()
