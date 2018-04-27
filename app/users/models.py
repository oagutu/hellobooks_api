"""
Endpoint user models."""

from app import db
from datetime import datetime, timedelta


class User(db.Model):
    """
    Represents user table"""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    acc_status = db.Column(db.String(40), default="member")
    borrowed_books = db.Column(db.PickleType, default={})

    def __init__(self, user_info):
        """
        Sets values of a book object."""

        self.name = user_info['name']
        self.email = user_info['email']
        self.username = user_info['username']
        self.password = user_info['password']

        if 'acc_status' in user_info:
            self.acc_status = user_info['acc_status']
        if 'borrowed_books' in  user_info:
            self.borrowed_books = user_info['borrowed_books']

    def add_to_reg(self):
        """
        Adds books to library dict."""
        # print(self)
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_user(username):
        """
        Fetches user details from register."""
        # print(User.query.filter(User.username == username))

        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_register():
        """
        Returns all users."""

        return User.query.all()

    def set_password(self, user_info):
        """
        Sets user password.
        User_info: list -> [username, current_password, new_password]
        """

        if self.password != user_info[2]:
            self.password = user_info[2]

    def get_all_borrowed(self):
        """
        Returns list of borrowed books by user"""

        return self.borrowed_books

    @staticmethod
    def set_borrowed():
        """
        Provides borrow/return book functionality."""

        borrow_info = dict()

        borrow_info["borrow_date"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        borrow_info["return_date"] = (datetime.now() + timedelta(days=10)).strftime(
            "%d/%m/%Y %H:%M")
        borrow_info["fee_owed"] = 0
        borrow_info["status"] = "valid"

        return borrow_info

    def add_to_borrowed(self, book_id, borrow_info):
        """
        Adds borrowed book to borrowed_books dictionary."""

        self.borrowed_books[book_id] = borrow_info
        db.session.commit()

    def update_borrowed(self, book_id, borrow_period):
        """
        Updates borrowed book info."""

        if borrow_period < 0:
            self.borrowed_books[book_id]["fee_owed"] = borrow_period * 30
        self.borrowed_books[book_id]["status"] = "returned"
        db.session.commit()

    def __repr__(self):
        """
        Represents the object instance of the model when queried."""
        return str({
            self.username: {
                "user_id": self.id,
                "name": self.name,
                "password": self.password,
                "email": self.email,
                "acc_status": self.acc_status,
                "borrowed_books": self.borrowed_books
            }
        })

    # def set_borrowed(self):
    #     """
    #     Provides borrow/return book functionality."""
    #
    #     book_info = dict()
    #
    #     book_info["borrow_date"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    #     book_info["return_date"] = (datetime.now() + timedelta(days=10)).strftime(
    #         "%d/%m/%Y %H:%M")
    #     book_info["fee_owed"] = 0
    #     book_info["status"] = "valid"
    #
    #     return book_info
    #
    # def get_borrowed(self, book_id):
    #     """
    #     Gets a book from the list of borrowed books by id."""
    #
    #     if self.borrowed_books[book_id]:
    #         return self.borrowed_books[book_id]
    #



# register = {
#     "John": {
#         "user_id": 2334,
#         "name": "John Paul",
#         "username": "John",
#         "email": "qwert@keyboard.com",
#         "password": "1234",
#         "acc_status": "member"
#     },
#     "Jane": {
#         "user_id": 4887,
#         "name": "Jane Doe",
#         "username": "Jane",
#         "email": "wasd@keyboard.com",
#         "password": "1234",
#         "acc_status": "admin"
#     },
#     "thatguy": {
#         'name': 'Baba',
#         'user_id': 1234,
#         'username': 'thatguy',
#         'password': 'qwerty',
#         'acc_status': 'suspended',
#         'borrowed_books': {}
#     }
# }
#
#
# class User(object):
#     """
#     Used to create user objects."""
#
#     def __init__(self):
#         """
#         Initializes user object"""
#
#         self.user_id = None
#         self.name = None
#         self.username = None
#         self.email = None
#         self.password = None
#         self.acc_status = None
#
#         self.borrowed_books = {
#             23: {
#                 "borrow_date": "25/04/2018 02:30",
#                 "return_date": "1/05/2018 02:30",
#                 "fee_owed": 0,
#                 "borrow_status": "valid"
#             },
#             24: {
#                 "borrow_date": "25/03/2018 02:30",
#                 "return_date": "1/04/2018 02:30",
#                 "fee_owed": 0,
#                 "borrow_status": "pending"
#             }
#         }
#
#
