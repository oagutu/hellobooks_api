"""
    tests/test_users/test_logout.py
    Provides testing for logoutendpoints.
"""

import unittest
from tests.test_users.test_users import UserEndpointsTestCase


class LogoutTestCase(UserEndpointsTestCase):
    """Test user API endpoints"""

    def test_logout(self):
        """Test logout"""

        result = self.client.post(
            'api/v1/auth/logout',
            headers={'Authorization': 'Bearer {}'.format(self.tokens['test_token'])})
        self.assertIn(b'Successfully logged out', result.data)


if __name__ == '__main__':
    unittest.main()
