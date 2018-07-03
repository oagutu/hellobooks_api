"""
    tests/test_books/test_update_book.py
    Provides testing forupdate  book endpoints.
"""

import unittest
import json
from tests.test_books.test_books import BookEndpointsTestCase


class UpdateBookTestCase(BookEndpointsTestCase):
    """Test book API endpoints"""

    def update(self, data, book_id, token):
        """Updates book in lib"""

        return self.client.put(
            '/api/v1/books/' + str(book_id),
            data=json.dumps(data),
            headers={"content-type": "application/json",
                     "Authorization": "Bearer {}".format(token)})

    def test_update_book_not_in_library(self):
        """Test updating book not in the library"""

        result = self.update(self.book_details, 3, self.tokens["Nickname"])
        self.assertEqual(result.status_code, 404)

    def test_update_book_in_library(self):
        """Test updating book in library"""

        result = self.update(self.book_details_two, 2, self.tokens["Nickname"])
        self.assertEqual(result.status_code, 202)
        self.assertIn(b'book title', result.data)
        self.assertIn(b'322.45', result.data)

    def test_update_book_unauthorised_account(self):
        """Test updating book by unauthorized account"""

        self.user(self.user_details_two)
        result = self.user({'username': 'thatguy', 'password': 'qwerty'}, False)
        token = result.headers['Authorization']

        result = self.update(self.book_details_two, 2, token)

        self.assertEqual(result.status_code, 403)
        self.assertIn(b'Unauthorised User', result.data)

    def test_update_book_invalid_book_id(self):
        """Test updating book while passing an invalid id."""

        result = self.update(self.book_details_two, "k", self.tokens["Nickname"])
        self.assertEqual(result.status_code, 404)


if __name__ == '__main__':
    unittest.main()
