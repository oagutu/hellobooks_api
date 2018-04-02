'''
    tests/test_users.py
    Provides testing for book endpoints 
'''

import unittest
import json

from app import create_app


class UserEndpointsTestCase(unittest.TestCase):
    '''Tests book API endpoints'''

    def setUp(self):
        '''sets up testing environment variables'''

        self.app = create_app('development')
        self.client = self.app.test_client()
        self.user_details ={
                "name": "Jane Doe",
                "user_id": 123456,
                "username": "JD",
                "password": "qwerty",
                "email": "abc@gfg.com",
                "acc_status": "member",
                "borrowed_books": {}
        }


    def test_create_user_account(self):
        '''tests create_user_account functionality'''

        result = self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details),
            headers={"content-type": "application/json"})
        print(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertIn(b'JD', result.data)
        self.assertIn(b'123456', result.data)

    def test_login_reset_logout(self):
        '''tests login(), reset_password() and logout() functionality'''

        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'JD', 'password': 'qwerty'}),
            headers={"content-type": "application/json"})
        self.assertIn(b'Successfully logged in', result.data)
        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'JD', 'password': 'rose'}),
            headers={"content-type": "application/json"})
        self.assertIn(b'Incorrect password', result.data)
        result = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'Amber', 'password': 'rose'}),
            headers={"content-type": "application/json"})
        self.assertIn(b'Account not available', result.data)

        #password reset test
        result = self.client.post(
            'api/v1/auth/reset-password',
            data=json.dumps({'username': 'JD', 'current_password': 'qwerty', 'new_password' : "09876"}),
            headers={"content-type": "application/json"})
        self.assertEqual(result.status_code, 202)
        self.assertIn(b'Successfully changed password', result.data)
        result=self.client.post(
            'api/v1/auth/reset-password',
            data = json.dumps({'username': 'JD', 'current_password': 'pass123', 'new_password': "09876"}),
            headers = {"content-type": "application/json"})
        self.assertIn(b'Current password incorrect', result.data)

        #logout test
        result = self.client.post(
            'api/v1/auth/logout')
        self.assertIn(b'Successfully logged out', result.data)


if __name__ == '__main__':
    unittest.main()
