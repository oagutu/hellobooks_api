"""
    tests/test_users/test_status_change.py
    Provides testing for user status change endpoints.
"""

import unittest
import json
from tests.test_users.test_users import UserEndpointsTestCase


class ChangeStatusTestCase(UserEndpointsTestCase):
    """Test user API endpoints"""

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

        self.assertEqual(self.user(self.user_details_two).status_code, 201)

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

        self.assertEqual(self.user(self.user_details_two).status_code, 201)

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

        self.assertEqual(self.user(self.user_details_two).status_code, 201)

        result = self.user({'username': 'John', 'password': 'qwerty'}, False)
        self.assertIn(b'Successfully logged in', result.data)
        token = result.headers['Authorization']

        result = self.client.put(
            '/api/v1/auth/users/status_change',
            data=json.dumps({'user': 1234, 'new_status': 'banned'}),
            headers={
                'content-type': 'application/json',
                'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(result.status_code, 405)


if __name__ == '__main__':
    unittest.main()
