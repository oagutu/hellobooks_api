'''
    tests/test_books.py
    Provides testing for book endpoints 
'''

import unittest
import json

from app import create_app

class BookEndpointsTestCase(unittest.TestCase):
    '''Tests book API endpoints'''
    
    def setUp(self):
        '''sets up testing environment'''
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

    def test_add_book(self):
        '''tests add book functionality'''

        result = self.client.post(
            "/api/v1/books",
            data = json.dumps(self.book_details),
            headers = {"content-type":"application/json"})
        self.assertEqual(result.status_code, 201)
        self.assertIn(b'book title', result.data)
        self.assertIn(b'12345', result.data)

    def test_update_book(self):
        '''
            Tests update_book() functionality
            checks if appropriate record updated
        '''
        self.assertEqual(self.client.post(
            '/api/v1/books',
            data = json.dumps(self.book_details),
            headers={"content-type": "application/json"}).status_code, 201)
        result = self.client.put('/api/v1/books/3',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 404)
        result = self.client.put('/api/v1/books/1',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 202)
        self.assertIn(b'book title', result.data)
        self.assertIn(b'12345', result.data)

    def test_remove_book(self):
        '''Tests remove_book() functionality'''

        self.assertEqual(self.client.post(
            '/api/v1/books',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json"}).status_code, 201)
        result = self.client.delete('/api/v1/books/3')
        self.assertEqual(result.status_code, 404)
        result = self.client.delete('/api/v1/books/1')
        self.assertEqual(result.status_code, 200)
        self.assertNotIn(b'book title', result.data)

    def test_retrieve_all_books(self):
        '''Tests retrieve_all_books() functionality'''

        self.assertEqual(self.client.post(
            '/api/v1/books',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json"}).status_code, 201)
        result = self.client.get(
            '/api/v1/books',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'book title', result.data)

    def test_get_book(self):
        '''tests get_book() functionality'''

        self.assertEqual(self.client.post(
            '/api/v1/books',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json"}).status_code, 201)
        result = self.client.get(
            '/api/v1/books/1',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 200)
        self.assertIn('book title', str(result.data))

    def test_borrow_return_book(self):
        '''
            tests borrow_return_book() functionality
           checks if book status changed to borrowed
        '''

        self.assertEqual(self.client.post(
            '/api/v1/books',
            data=json.dumps(self.book_details),
            headers={"content-type": "application/json"}).status_code, 201)
        result = self.client.post(
            '/api/v1/users/books/1',
            data=json.dumps(self.user_details),
            headers={"content-type": "application/json"})
        self.assertIn(b'borrowed', result.data)

        result = self.client.post(
            '/api/v1/users/books/1',
            data=json.dumps(self.user_details),
            headers={"content-type": "application/json"})
        self.assertIn(b'returned', result.data)



if __name__ == '__main__':
    unittest.main()

#TODO: fix test_borrow_return datetime format conflict
