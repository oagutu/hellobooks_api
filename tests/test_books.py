"""
    tests/test_books.py
    Provides testing for book endpoints.
"""

import unittest
import json

from app import create_app, db


class BookEndpointsTestCase(unittest.TestCase):
    """
    Tests book API endpoints"""
    
    def setUp(self):
        """
        Sets up testing environment."""

        self.app = create_app('development')
        self.client = self.app.test_client()

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

        self.book_details = {
            "book_id": 1,
            "title": "book title",
            "book_code": 978966433901,
            "ddc_code": "321.45",
            "author": "mary",
            "synopsis": "Pef ohew ouweq...",
            "genre": 'fiction',
            "sub_genre": "xyz",
        }
        self.book_details_two = {
            "book_id": 2,
            "title": "book title two",
            "book_code": 978962222901,
            "ddc_code": "322.45",
            "author": "poppins",
            "genre": "non-fiction",
            "status": "borrowed"
        }
        self.book_details_three = {
            "book_id": 3,
            "title": "book title two",
            "book_code": 978962221234,
            "ddc_code": "322.00",
            "author": "po",
            "genre": "fiction",
            "subgenre": "legal-drama",
            "status": "borrowed"
        }

        self.user_details = {
            'name': 'John Doe',
            'user_id': '123456',
            'email': 'name@email.co.ke',
            'username': 'Nickname',
            'password': 'qwerty',
            'acc_status': 'admin',
            'borrowed_books': {
                2: {
                    "title": "book title two",
                    "book_code": 978962222901,
                    "borrow_date": "25/04/2018 02:30",
                    "ERD": "30/04/2018 02:30",
                    "return_date": "1/05/2018 02:30",
                    "fee_owed": 0,
                    "borrow_status": "valid"},
                4: {
                    "title": "book title three",
                    "book_code": 978933322901,
                    "borrow_date": "21/04/2018 02:30",
                    "ERD": "29/04/2018 02:30",
                    "return_date": "29/04/2018 02:30",
                    "fee_owed": 0,
                    "borrow_status": "invalid"
                }
            }
        }

        self.user_details_two = {
            'name': 'Baba',
            'user_id': '1234',
            'username': 'thatguy',
            'password': 'qwerty',
            'email': 'jina@email.co.ke',
            'acc_status': 'suspended',
            'borrowed_books': {}}

        self.tokens = {}

        self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details),
            headers={"content-type": "application/json"})

        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'Nickname', 'password': 'qwerty'}),
            headers={"content-type": "application/json"})
        # print(result.data)
        self.tokens['Nickname'] = result.headers['Authorization']

        self.client.post(
            "/api/v1/books",
            data=json.dumps(self.book_details_two),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def test_add_book(self):
        """
        Tests add book functionality."""

        result = self.client.post(
            "/api/v1/books",
            data=json.dumps(self.book_details),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        # print(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertIn(b'book title', result.data)
        self.assertIn(b'321.45', result.data)

    def test_add_book_invalid_title(self):
        """
        Tests add book functionality for an invalid title."""

        result = self.client.post(
            "/api/v1/books",
            data=json.dumps({
                "book_id": 1,
                "title": " ",
                "book_code": "123.45",
                "author": "mary writer",
                "genre": "fiction",
            }),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'Invalid title', result.data)

    def test_add_book_invalid_author(self):
        """
        Tests add book functionality for an invalid author."""

        result = self.client.post(
            "/api/v1/books",
            data=json.dumps({
                "book_id": 1,
                "title": "book title here",
                "book_code": "123.45",
                "author": "",
                "genre": "fiction",
            }),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'Invalid author', result.data)

    def test_add_book_missing_ddc_code(self):
        """
        Tests add book functionality for an missing book_code."""
        result = self.client.post(
            "/api/v1/books",
            data=json.dumps({
                "book_id": 1,
                "title": "yyy",
                "book_code": 970066433901,
                "author": "mary writer",
                "genre": "non-fiction",
            }),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertIn(b'Missing ddc Code', result.data)

    def test_add_book_invalid_ddc_code(self):
        """
        Tests add book functionality for an invalid ddc_code."""

        result = self.client.post(
            "/api/v1/books",
            data=json.dumps({
                "book_id": 1,
                "title": "yyy",
                "book_code": 970066433901,
                "ddc_code": "pp",
                "author": "mary writer",
                "genre": "fiction",
            }),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        print(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'Invalid ddc_code', result.data)

    def test_add_book_missing_book_code(self):
        """
        Tests add book functionality for an missing book_code."""

        result = self.client.post(
            "/api/v1/books",
            data=json.dumps({
                "book_id": 1,
                "title": "yyy",
                "ddc_code": "123.45",
                "author": "mary writer",
                "genre": "fiction",
            }),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertIn(b'Missing book Code', result.data)

    def test_add_book_invalid_book_code(self):
        """
        Tests add book functionality for an invalid book_code.
        Book code can either be already existing or have an invalid format"""

        result = self.client.post(
            "/api/v1/books",
            data=json.dumps(self.book_details_two),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertIn(b'Book(book_code) already in lib', result.data)

        result = self.client.post(
            "/api/v1/books",
            data=json.dumps({
                "book_id": 1,
                "title": "yyy",
                "book_code": 9700664339,
                "ddc_code": "123.45",
                "author": "mary writer",
                "genre": "fiction",
            }),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertIn(b'Invalid book_code', result.data)

    def test_add_book_unauthorized_account(self):
        """
        Tests adding a book by an unauthorised account ie. not an admin"""

        self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details_two),
            headers={"content-type": "application/json"})

        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'thatguy', 'password': 'qwerty'}),
            headers={"content-type": "application/json"})
        token = result.headers['Authorization']

        result = self.client.post(
            "/api/v1/books",
            data=json.dumps(self.book_details),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(token)})
        self.assertIn(b'Account not authorised to perform selected function', result.data)

    def test_update_book_not_in_library(self):
        """
        Tests upadting book not in the library"""

        result = self.client.put('/api/v1/books/3',
                                 data=json.dumps(self.book_details),
                                 headers={"content-type": "application/json",
                                          'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 404)

    def test_update_book_in_library(self):
        """
        Tests updating book in library"""

        result = self.client.put('/api/v1/books/2',
                                 data=json.dumps(self.book_details_two),
                                 headers={"content-type": "application/json",
                                          'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 202)
        self.assertIn(b'book title', result.data)
        self.assertIn(b'322.45', result.data)

    def test_update_book_unauthorised_account(self):
        """Tests updating book by unauthorized account"""

        self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details_two),
            headers={"content-type": "application/json"})

        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'thatguy', 'password': 'qwerty'}),
            headers={"content-type": "application/json"})
        token = result.headers['Authorization']

        result = self.client.put('/api/v1/books/2',
                                 data=json.dumps(self.book_details_two),
                                 headers={"content-type": "application/json",
                                          'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(result.status_code, 401)
        self.assertIn(b'Account not authorised to perform selected function', result.data)

    def test_remove_book(self):
        """
        Tests remove_book() functionality"""

        result = self.client.delete('/api/v1/books/3',
                                    headers={'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 404)

        result = self.client.delete('/api/v1/books/2',
                                    headers={'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 204)
        self.assertNotIn(b'book title', result.data)

    def test_remove_book_unauthorised_account(self):
        """Tests updating book by unauthorized account"""

        self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details_two),
            headers={"content-type": "application/json"})

        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'thatguy', 'password': 'qwerty'}),
            headers={"content-type": "application/json"})
        token = result.headers['Authorization']

        result = self.client.delete('/api/v1/books/2',
                                    headers={'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(result.status_code, 401)
        self.assertIn(b'Account not authorised to perform selected function', result.data)

    def test_retrieve_all_books(self):
        """
        Tests retrieve_all_books() functionality."""

        self.assertEqual(self.client.post(
            '/api/v1/books',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])}).status_code, 201)
        result = self.client.get('/api/v1/books?results=1',
                                 headers={'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'book title', result.data)

    def test_retrieve_all_books_invalid_page(self):
        """
        Tests retrieve_all_books() functionality for missing page."""

        self.assertEqual(self.client.post(
            '/api/v1/books',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])}).status_code, 201)
        result = self.client.get('/api/v1/books?results=1&page=3',
                                 headers={'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 404)

    def test_get_book(self):
        """
        Tests get_book() functionality"""

        self.assertEqual(self.client.post(
            '/api/v1/books',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])}).status_code, 201)
        result = self.client.get(
            '/api/v1/books/1',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 200)
        self.assertIn('book title', str(result.data))

    def test_get_book_not_in_libary(self):
        """
        Tests getting book not in library."""

        self.assertEqual(self.client.get(
            '/api/v1/books/10',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])}).status_code, 404)

    def test_borrow_book(self):
        """
        Tests borrowing book
        checks if book status changed to borrowed.
        """
        self.client.post(
            "/api/v1/books",
            data=json.dumps(self.book_details),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})

        result = self.client.post(
            '/api/v1/users/books/1',
            headers={
                'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertIn(b'borrowed', result.data)

    def test_borrow_book_not_in_library(self):
        """
        Tests borrowing book not in library"""

        result = self.client.post(
            '/api/v1/users/books/11',
            headers={
                'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertIn(b'Book not available', result.data)
        self.assertEqual(result.status_code, 404)

    def test_return(self):
        """
        Tests returning a book."""

        result = self.client.put(
            '/api/v1/users/books/2',
            headers={
                'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertIn(b'returned', result.data)

    def test_return_book_not_borrowed(self):
        """
        Tests returning book not borrowed by user."""

        self.client.post(
            "/api/v1/books",
            data=json.dumps(self.book_details_three),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})

        result = self.client.put(
             '/api/v1/users/books/3',
             headers={
                 'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertIn(b'cannot return book. Not borrowed by user', result.data)

    def test_user_not_authorized_to_borrow(self):
        """
        Tests book borrowing by unauthorized user"""

        self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details_two),
            headers={"content-type": "application/json"})

        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'thatguy', 'password': 'qwerty'}),
            headers={"content-type": "application/json"})
        token = result.headers['Authorization']
    
        result = self.client.post(
            '/api/v1/users/books/2',
            headers={
                'Authorization': 'Bearer {}'.format(token)})
        self.assertIn(
                b'Member currently not authorised to borrow book', result.data)

    def test_get_user_borrow_history(self):
        """
        Tests getting user borrowing history"""

        result = self.client.get(
            '/api/v1/users/books?results=5&order_param=borrow_date',
            headers={
                'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        # print("test_books: ", result.data)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'book title two', result.data)

    def test_get_user_not_returned_books(self):
        """
        Tests getting books not returned by user"""

        result = self.client.get(
            '/api/v1/users/books?returned=false',
            headers={
                'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 200)
        self.assertNotIn(b'book title two', result.data)
        self.assertIn(b'book title three', result.data)

    def test_get_add_log(self):
        """
        Test if data logged."""

        result = self.client.get(
            '/api/v1/users/books/logs?book_id=2',
            headers={
                'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'2', result.data)

    def test_get_add_log_unauthorised_user(self):
        """
        Test if data logged."""

        self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details_two),
            headers={"content-type": "application/json"})

        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'thatguy', 'password': 'qwerty'}),
            headers={"content-type": "application/json"})
        token = result.headers['Authorization']

        result = self.client.get(
            '/api/v1/users/books/logs',
            headers={
                'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(result.status_code, 401)
        self.assertIn(b'User not authorised', result.data)

    def test_get_update_log(self):
        """
        Test getting log of updated book"""

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
        """
        Test getting log of updated book"""

        self.assertEqual(
            self.client.delete(
                '/api/v1/books/2',
                headers={'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])}).status_code, 204)

        result = self.client.get(
            '/api/v1/users/books/logs',
            headers={
                'Authorization': 'Bearer {}'.format(self.tokens["Nickname"])})
        print(result.data)
        self.assertIn(b'DELETE', result.data)


if __name__ == '__main__':
    unittest.main()
