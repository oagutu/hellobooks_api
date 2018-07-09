"""
    tests/test_books/test_add_book.p[y
    Provides testing for book endpoints.
"""

import unittest
from test_books import BookEndpointsTestCase


class AddBookTestCase(BookEndpointsTestCase):
    """Test book API endpoints"""

    def test_add_book(self):
        """Test add book functionality."""

        result = self.add(self.tokens["Nickname"], self.book_details)
        self.assertEqual(result.status_code, 201)
        self.assertIn(b'Book title', result.data)
        self.assertIn(b'321.45', result.data)

    def test_add_book_invalid_title(self):
        """Test add book functionality for an invalid title."""

        book = {
                "book_id": 1,
                "title": " ",
                "book_code": "123.45",
                "author": "mary writer",
                "genre": "fiction",
            }
        result = self.add(self.tokens["Nickname"], book)

        self.assertEqual(result.status_code, 400)
        self.assertIn(b'Invalid title', result.data)

    def test_add_book_invalid_author(self):
        """Test add book functionality for an invalid author."""

        book = {
                "book_id": 1,
                "title": "book title here",
                "book_code": "123.45",
                "author": "",
                "genre": "fiction",
            }
        result = self.add(self.tokens["Nickname"], book)

        self.assertEqual(result.status_code, 400)
        self.assertIn(b'Invalid author', result.data)

    def test_add_book_missing_ddc_code(self):
        """Test add book functionality for an missing book_code."""

        book = {
                "book_id": 1,
                "title": "yyy",
                "book_code": 970066433901,
                "author": "mary writer",
                "genre": "non-fiction",
            }
        result = self.add(self.tokens["Nickname"], book)

        self.assertIn(b'Missing ddc Code', result.data)

    def test_add_book_invalid_ddc_code(self):
        """Test add book functionality for an invalid ddc_code."""

        book = {
                "book_id": 1,
                "title": "yyy",
                "book_code": 970066433901,
                "ddc_code": "pp",
                "author": "mary writer",
                "genre": "fiction",
            }
        result = self.add(self.tokens["Nickname"], book)

        self.assertEqual(result.status_code, 400)
        self.assertIn(b'Invalid ddc_code', result.data)

    def test_add_book_missing_book_code(self):
        """Test add book functionality for an missing book_code."""

        book = {
                "book_id": 1,
                "title": "yyy",
                "ddc_code": "123.45",
                "author": "mary writer",
                "genre": "fiction",
            }
        result = self.add(self.tokens["Nickname"], book)

        self.assertIn(b'Missing book Code', result.data)

    def test_add_book_invalid_book_code(self):
        """
        Test add book functionality for an invalid book_code.

        Book code can either be already existing or have an invalid format.
        """

        result = self.add(self.tokens["Nickname"], self.book_details_two)
        self.assertIn(b'Book(book_code) already in lib', result.data)

        book = {
                "book_id": 1,
                "title": "yyy",
                "book_code": 9700664339,
                "ddc_code": "123.45",
                "author": "mary writer",
                "genre": "fiction",
            }
        result = self.add(self.tokens["Nickname"], book)

        self.assertIn(b'Invalid book_code', result.data)

    def test_add_book_unauthorized_account(self):
        """Test adding a book by an unauthorised account ie. not an admin"""

        self.user(self.user_details_two)
        result = self.user({'username': 'thatguy', 'password': 'qwerty'}, False)
        token = result.headers['Authorization']
        result = self.add(token, self.book_details)

        self.assertIn(b'Unauthorised User', result.data)


if __name__ == '__main__':
    unittest.main()
