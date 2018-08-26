"""
    tests/test_books/test_update_book.py
    Provides testing forupdate  book endpoints.
"""

import unittest
import json
from tests.test_books.test_books import BookEndpointsTestCase


class BookLogsTestCase(BookEndpointsTestCase):
    """Test book API endpoints"""

    def test_get_add_log(self):
        """Test if data logged."""

        result = self.client.get(
            '/api/v1/users/books/logs?book_id=2',
            headers={
                'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'2', result.data)

    def test_get_add_log_unauthorised_user(self):
        """Test that unauthorised user cannot access book logs"""

        self.user(self.user_details_two)
        result = self.user({'username': 'thatguy', 'password': 'qwerty'}, False)
        token = result.headers['Authorization']

        result = self.client.get(
            '/api/v1/users/books/logs',
            headers={
                'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(result.status_code, 403)
        self.assertIn(b'Unauthorised User', result.data)

    def test_get_update_log(self):
        """Test getting log of updated book"""

        self.assertEqual(self.client.put('/api/v1/books/2',
                         data=json.dumps(self.book_details_two),
                         headers={"content-type": "application/json",
                                  'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])}).status_code, 202)

        result = self.client.get(
            '/api/v1/users/books/logs',
            headers={
                'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertIn(b'UPDATE', result.data)

    def test_get_delete_log(self):
        """Test getting log of deleted book"""

        self.assertEqual(
            self.client.delete(
                '/api/v1/books/2',
                headers={'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])}).status_code, 204)

        result = self.client.get(
            '/api/v1/users/books/logs',
            headers={
                'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertIn(b'DELETE', result.data)


if __name__ == '__main__':
    unittest.main()
