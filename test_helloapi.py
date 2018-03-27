'''Testing of the various api endpoints'''

import unittest
from app import create_app


class ApiEndpoint(unittest.TestCase):
    '''Class holds the api endpoint test functions '''

    def setUp(self):
        '''sets up necessary variables before each test case'''

        self.app = create_app('development')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context().push()

        self.book_details = {'id': 1, 'title': 'book title', 'code': 12345, 'author': 'mary writer', 'synopsis': "iwehn owueh owunef ohew ouweq...",
                             'genre': 'fiction', 'sub_genre': 'xyz', 'status': 'available'}
        self.user_details = {'name': 'John Doe', 'user_id': '123456',
                             'username': 'Jane Doe', 'password': 'qwerty', 'acc_type': 'member'}

    def test_add_book(self):
        '''
            Tests add_book() functionality
            verifies: database correctly updated
        '''
        result = self.client.post('/api/books/', data=self.book_details)
        print(result)
        self.assertEqual(result.status_code, 201)
        self.assertIn(self.book_details['title'], result.data)
        self.assertIn(self.book_details['code'], str(result.data))

    def test_update_book(self):
        '''
            Tests update_book() functionality
            checks if appropriate record updated
        '''
        self.assertEqual(self.client.post(
            'api/books', data=self.book_details).status_code, 201)
        result = self.client.put('/api/books/1', data={'code': 54321})
        self.assertIn(self.book_details['title'], str(result.data))
        self.assertIn(54321, str(result.data))

    def test_remove_book(self):
        '''Tests remove_book() functionality'''

        self.assertEqual(self.client.post(
            'api/books', data=self.book_details).status_code, 201)
        result = self.client.delete('/api/books/1')
        self.assertEqual(result.status_code, 200)
        self.assertNotIn('book title', str(result.data))

    def test_retrieve_all_books(self):
        '''Tests retrieve_all_books() functionality'''

        self.assertEqual(self.client.post(
            'api/books', data=self.book_details).status_code, 201)
        result = self.client.get('/api/books')
        self.assertEqual(result.status_code, 200)
        self.assertIn(self.book_details, str(result.data))
        #only one item/book added therefore only 1 entry returned
        self.assertEqual(len(result.data), 1)

    def test_get_book(self):
        '''tests get_book() functionality'''

        self.assertEqual(self.client.post(
            'api/books', data=self.book_details).status_code, 201)
        result = self.client.get('/api/books/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('book title', str(result.data))
        # only 1 item/book should be returned
        self.assertEqual(len(result.data), 1)

    def test_borrow_return_book(self):
        '''
            tests borrow_return_book() functionality
           checks if book status changed to borrowed
        '''

        self.assertEqual(self.client.post(
            'api/books', data=self.book_details).status_code, 201)
        result = self.client.post('/api/users/books/1', data=self.book_details)
        self.assertIn('borrowed', str(result.data))

        result = self.client.post('/api/users/books/1', data=self.book_details)
        self.assertIn('returned', str(result.data))

    def test_create_user_account(self):
        '''tests create_user_account() functionality'''

        result = self.client.post('/api/auth/register',
                                  data=self.user_details)
        self.assertEqual(result.status_code, 201)
        self.assertIn('John Doe', str(result.data))

    def test_user_login_logout(self):
        '''tests user_login() functionality'''

        self.assertEqual(self.client.post('/api/auth/register',
                                          data=self.user_details).status_code, 201)
        result = self.client.post(' /api/auth/login', 
                                  data = {'username':'Jane Doe', 'password':'qwerty'})
        self.assertIn('Successfully logged in', str(result.data))

        result = self.client.post('/api/auth/logout')
        self.assertIn('Successfully logged out', str(result.data))

    def test_reset_password(self):
        '''tests reset_password() functionality'''

        self.assertEqual(self.client.post('/api/auth/register',
                                          data=self.user_details).status_code, 201)
        self.client.post(' /api/auth/login',
                         data={'username': 'Jane Doe', 'password': 'qwerty'})
        result = self.client.post('/api/auth/reset-password', data = {'password':'new_password'})
        self.assertEqual(result.status_code, 201)
        self.assertNotIn(self.user_details['password'], str(result.data))
        #checks to see new password not equal to old password


if __name__ == '__main__':
    unittest.main()
