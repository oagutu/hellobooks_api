"""
    tests/test_users.py
    Provides testing for book endpoints.
"""

import unittest
import json

from app import create_app, db


class UserEndpointsTestCase(unittest.TestCase):
    """Test user API endpoints."""

    def setUp(self):
        """et up testing environment variables."""

        self.app = create_app('testing')
        self.client = self.app.test_client()

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

        self.user_details = {
            "name": "Jane Doe",
            "user_id": 123456,
            "username": "JD",
            "password": "qwerty",
            "confirm_password": "qwerty",
            "email": "abc@gfg.com",
            "acc_status": "member",
            "borrowed_books": {}
        }

        self.user_details_two = {
            "name": "Baba",
            "user_id": 1234,
            "username": "John",
            "password": "qwerty",
            "confirm_password": "qwerty",
            "email": "qwerty@keyboard.com",
            "acc_status": "suspended",
            "borrowed_books": {}}

        self.user_details_four = {
            "name": "John Doe",
            "user_id": 654321,
            "username": "Doe",
            "password": "qwerty",
            "confirm_password": "qwerty",
            "email": "abc@test.com",
            "acc_status": "admin",
            "borrowed_books": {}
        }

        self.tokens = {}

        r = self.client.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_details_four),
            headers={"content-type": "application/json"})

        res = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({'username': 'Doe', 'password': 'qwerty'}),
            headers={"content-type": "application/json"})
        self.tokens['test_token'] = res.headers['Authorization']

    def tearDown(self):
        """teardown all initialized variables."""
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
        # login
        else:
            return self.client.post(
                "/api/v1/auth/login",
                data=json.dumps(data),
                headers={"content-type": "application/json"})
