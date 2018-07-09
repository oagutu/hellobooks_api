"""
    tests/test_books/test_remove_book.py
    Provides testing for remove book endpoints.
"""

import unittest
from test_books import BookEndpointsTestCase


class RemoveBookTestCase(BookEndpointsTestCase):
    """Test book API endpoints"""

    def test_remove_book(self):
        """Test remove_book() functionality"""

        result = self.client.delete('/api/v1/books/3',
                                    headers={'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 404)

        result = self.client.delete('/api/v1/books/2',
                                    headers={'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 204)
        self.assertNotIn(b'book title', result.data)

    def test_remove_book_unauthorised_account(self):
        """Test updating book by unauthorized account"""

        self.user(self.user_details_two)
        result = self.user({'username': 'thatguy', 'password': 'qwerty'}, False)
        token = result.headers['Authorization']

        result = self.client.delete('/api/v1/books/2',
                                    headers={'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(result.status_code, 403)
        self.assertIn(b'Unauthorised User', result.data)


if __name__ == '__main__':
    unittest.main()
