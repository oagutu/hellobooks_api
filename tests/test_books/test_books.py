"""
    tests/test_books.py
    Provides testing for book endpoints.
"""

import unittest
import json

from app import create_app, db


class BookEndpointsTestCase(unittest.TestCase):
    """Test book API endpoints"""
    
    def setUp(self):
        """Set up testing environment."""

        self.app = create_app('testing')
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
            'acc_status': 'admin'
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

        # Register user.
        self.user(self.user_details)
        # User login
        result = self.user({'username': 'Nickname', 'password': 'qwerty'}, False)
        self.tokens['Nickname'] = result.headers['Authorization']

        self.add(self.tokens["Nickname"], self.book_details_two)

    def tearDown(self):
        """Teardown all initialized variables."""

        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def user(self, data, register=True):
        """
        Register or logina user.

        :param data: user details
        :type data: dict
        :param register: indicates if registering user(True) or logging in(False)
        :type register: Bool
        :return: JSON response obj
        """

        # Register new user
        if register:
            return self.client.post(
                "/api/v1/auth/register",
                data=json.dumps(data),
                headers={"content-type": "application/json"})
        else:
            return self.client.post(
                "/api/v1/auth/login",
                data=json.dumps(data),
                headers={"content-type": "application/json"})

    def add(self, token, data):
        """
        Add book.

        :param token: uer access token
        :param data: book details to be added
        :return: JSON response obj
        """
        return self.client.post(
            "/api/v1/books",
            data=json.dumps(data),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(token)})

    def borrow(self, url, token, book_id, method="POST"):
        """
        Access borrow book endpoints(borrow, return and get history.

        :param method: method to be used to access endpoint
        :type method:str
        :param url: endpoint url
        :type url:str
        :param book_id: id of book to be borrowed/returned
        :type book_id:int or None
        :param token: access_token
        :type token: str
        :return: JSON response obj
        """

        # Borrow book.
        if method == "POST":
            return self.client.post(
                url + str(book_id),
                headers={'Authorization': 'Bearer {}'.format(token)})

        # Return book.
        elif method == "PUT":
            return self.client.put(
                url + str(book_id),
                headers={'Authorization': 'Bearer {}'.format(token)})
        else:
            return self.client.get(url, headers={'Authorization': 'Bearer {}'.format(token)})


if __name__ == '__main__':
    unittest.main()
