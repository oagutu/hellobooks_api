"""
    tests/test_books.py
    Provides testing for book endpoints.
"""

import unittest
import json

from app import create_app


class BookEndpointsTestCase(unittest.TestCase):
    """
    Tests book API endpoints"""
    
    def setUp(self):
        """
        Sets up testing environment."""

        self.app = create_app('development')
        self.client = self.app.test_client()

        self.book_details = {
            "book_id": 1,
            "title": "book title",
            "book_code": 12345,
            "author": "mary writer",
            "synopsis": "Iwehn owueh owunef ohew ouweq...",
            "genre": "fiction",
            "subgenre": "xyz",
            "status": "available"
        }

        self.user_details = {
            'name': 'John Doe',
            'user_id': '123456',
            'username': 'Nickname',
            'password': 'qwerty',
            'acc_status': 'member',
            'borrowed_books': {}}

        self.user_details_two = {
            'name': 'Baba',
            'user_id': '1234',
            'username': 'thatguy',
            'password': 'qwerty',
            'acc_status': 'suspended',
            'borrowed_books': {}}

        self.tokens = {}

        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'Jane', 'password': '1234'}),
            headers={"content-type": "application/json"})
        self.tokens['Jane'] = result.headers['Authorization']

        self.client.post(
            '/api/v1/books',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json"})

    def test_add_book(self):
        """
        Tests add book functionality."""

        result = self.client.post(
            "/api/v1/books",
            data=json.dumps(self.book_details),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(self.tokens["Jane"])})
        self.assertEqual(result.status_code, 201)
        self.assertIn(b'book title', result.data)
        self.assertIn(b'12345', result.data)

    def test_update_book_not_in_library(self):
        """
        Tests upadting book not in the library"""

        result = self.client.put('/api/v1/books/3',
                                 data=json.dumps(self.book_details),
                                 headers={"content-type": "application/json",
                                          'Authorization': 'Bearer {}'.format(self.tokens["Jane"])})
        self.assertEqual(result.status_code, 404)

    def test_update_book_in_library(self):
        """
        Tests updating book in library"""

        result = self.client.put('/api/v1/books/1',
                                 data=json.dumps(self.book_details),
                                 headers={"content-type": "application/json",
                                          'Authorization': 'Bearer {}'.format(self.tokens["Jane"])})
        self.assertEqual(result.status_code, 202)
        self.assertIn(b'book title', result.data)
        self.assertIn(b'12345', result.data)

    def test_remove_book(self):
        """
        Tests remove_book() functionality"""

        result = self.client.delete('/api/v1/books/3',
                                    headers={'Authorization': 'Bearer {}'.format(self.tokens["Jane"])})
        self.assertEqual(result.status_code, 404)
        
        result = self.client.delete('/api/v1/books/1',
                                    headers={'Authorization': 'Bearer {}'.format(self.tokens["Jane"])})
        self.assertEqual(result.status_code, 204)
        self.assertNotIn(b'book title', result.data)

    def test_retrieve_all_books(self):
        """
        Tests retrieve_all_books() functionality."""

        self.assertEqual(self.client.post(
            '/api/v1/books',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Jane"])}).status_code, 201)
        result = self.client.get('/api/v1/books',
                                 headers={'Authorization': 'Bearer {}'.format(self.tokens["Jane"])})
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'book title', result.data)

    def test_get_book(self):
        """
        Tests get_book() functionality"""

        self.assertEqual(self.client.post(
            '/api/v1/books',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Jane"])}).status_code, 201)
        result = self.client.get(
            '/api/v1/books/1',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Jane"])})
        self.assertEqual(result.status_code, 200)
        self.assertIn('book title', str(result.data))

    def test_get_book_not_in_libary(self):
        """
        Tests getting book not in library."""

        self.assertEqual(self.client.get(
            '/api/v1/books/10',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Jane"])}).status_code, 404)

    def test_borrow_book(self):
        """
        Tests borrow_return_book() functionality
        checks if book status changed to borrowed
        """
        result = self.client.post(
            '/api/v1/users/books/1',
            data=json.dumps(self.user_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Jane"])})
        self.assertIn(b'borrowed', result.data)

    def test_return(self):
        """
        Tests returning a book."""

        result = self.client.post(
            '/api/v1/users/books/1',
            data=json.dumps(self.user_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Jane"])})
        self.assertIn(b'borrowed', result.data)

        result = self.client.post(
            '/api/v1/users/books/1',
            data=json.dumps(self.user_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Jane"])})
        self.assertIn(b'returned', result.data)

    def test_return_book_not_borrowed(self):
        """
        Tests returning book not borrowed by user"""

        result = self.client.post(
             '/api/v1/users/books/2',
             data=json.dumps(self.user_details),
             headers={"content-type": "application/json",
                      'Authorization': 'Bearer {}'.format(self.tokens["Jane"])})
        self.assertIn(b'cannot return book. Not borrowed by user', result.data)

    def test_user_not_authorized_to_borrow(self):
        """
        Tests book borrowing by unauthorized user"""
    
        result = self.client.post(
            '/api/v1/users/books/1',
            data=json.dumps(self.user_details_two),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Jane"])})
        self.assertIn(
                b'Member currently not authorised to borrow book', result.data)

    def test_borrow_book_not_in_library(self):
        """
        Tests borrowing book not in library"""

        result = self.client.post(
            '/api/v1/users/books/11',
            data=json.dumps(self.user_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Jane"])})
        self.assertIn(b'Book not avialable', result.data)
        self.assertEqual(result.status_code, 404)


if __name__ == '__main__':
    unittest.main()
