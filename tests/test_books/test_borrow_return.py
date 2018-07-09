"""
    tests/test_books/test_borrow_return.py
    Provides testing for borrow_return book endpoints.
"""

import unittest
from test_books import BookEndpointsTestCase


class RemoveBookTestCase(BookEndpointsTestCase):
    """Test book API endpoints"""

    def test_borrow_return_book(self):
        """
        Test borrowing and returning a book.

        checks if book status changed to borrowed.
        """

        self.add(self.tokens["Nickname"], self.book_details)

        # Test borrow book.
        result = self.borrow('/api/v1/users/books/', self.tokens["Nickname"], 1)
        self.assertIn(b'borrow_date', result.data)

        # Test returning book.
        result = self.borrow('/api/v1/users/books/', self.tokens['Nickname'], 1, 'PUT')
        self.assertIn(b'returned', result.data)

    def test_borrow_book_not_in_library(self):
        """Test borrowing book not in library."""

        result = self.borrow('/api/v1/users/books/', self.tokens["Nickname"], 11)
        self.assertIn(b'Book not available', result.data)
        self.assertEqual(result.status_code, 404)

    def test_return_book_not_borrowed(self):
        """Test returning book not borrowed by user."""

        self.add(self.tokens["Nickname"], self.book_details_three)

        result = self.borrow('/api/v1/users/books/', self.tokens['Nickname'], 3, 'PUT')
        self.assertIn(b'cannot return book. Not borrowed by user', result.data)

    def test_user_not_authorized_to_borrow(self):
        """Test book borrowing by unauthorized user"""

        self.user(self.user_details_two)
        result = self.user({'username': 'thatguy', 'password': 'qwerty'}, False)
        token = result.headers['Authorization']

        result = self.borrow('/api/v1/users/books/', token, 12)
        self.assertIn(b'Member currently not authorised to borrow book', result.data)

    def test_get_user_borrow_history(self):
        """Test getting user borrowing history"""

        self.add(self.tokens["Nickname"], self.book_details)
        self.borrow('/api/v1/users/books/', self.tokens["Nickname"], 1)

        result = self.borrow('/api/v1/users/books?order_param=borrow_date', self.tokens["Nickname"], None, "GET")

        self.assertEqual(result.status_code, 200)
        self.assertIn(b'book title', result.data)

    def test_get_user_not_returned_books(self):
        """Test getting books not returned by user"""

        self.add(self.tokens["Nickname"], self.book_details)
        self.borrow('/api/v1/users/books/', self.tokens["Nickname"], 1)
        self.borrow('/api/v1/users/books/', self.tokens["Nickname"], 2)
        self.borrow('/api/v1/users/books/', self.tokens["Nickname"], 2)

        result = self.borrow('/api/v1/users/books?returned=false', self.tokens["Nickname"], None, "GET")

        self.assertEqual(result.status_code, 200)
        self.assertNotIn(b'book title two', result.data)
        self.assertIn(b'book title', result.data)


if __name__ == '__main__':
    unittest.main()
