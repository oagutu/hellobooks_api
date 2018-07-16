"""
    tests/test_books/test_get_books.py
    Provides testing fetch book endpoints.
"""

import unittest
import json
from test_books import BookEndpointsTestCase


class GetBookTestCase(BookEndpointsTestCase):
    """Test book API endpoints"""

    def test_retrieve_all_books(self):
        """Test retrieve_all_books() functionality."""

        self.assertEqual(self.client.post(
            '/api/v1/books',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])}).status_code, 201)
        result = self.client.get('/api/v1/books?results=1',
                                 headers={'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Book title', result.data)

    def test_retrieve_all_books_invalid_page(self):
        """Test retrieve_all_books() functionality for missing page."""

        self.assertEqual(self.client.post(
            '/api/v1/books',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])}).status_code, 201)
        result = self.client.get('/api/v1/books?page=3',
                                 headers={'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 404)

    def test_get_book(self):
        """Test get_book() functionality"""

        self.add(self.tokens["Nickname"], self.book_details)
        result = self.client.get(
            '/api/v1/books/1',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 200)
        self.assertIn('book title', str(result.data).lower())

    def test_get_book_by_title(self):
        """Test searching for book using title, author"""

        self.add(self.tokens["Nickname"], self.book_details)
        result = self.client.get(
            '/api/v1/books/search?q=book title',
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 200)
        self.assertIn('Book title', str(result.data))

    def test_get_book_not_in_libary(self):
        """Test getting book not in library."""

        self.assertEqual(self.client.get(
            '/api/v1/books/10',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])}).status_code, 404)


if __name__ == '__main__':
    unittest.main()
