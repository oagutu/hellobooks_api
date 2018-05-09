"""
Endpoint user models."""

from app import db
from datetime import datetime, timedelta

from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.ext.declarative import declarative_base


class MutableDict(Mutable, dict):
    """
    Represents MutableDict object."""

    @classmethod
    def coerce(cls, key, value):
        """
        Converts dictionary to MutableDict type"""

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        """
        Handles set events for MutableDict."""

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        """
        Handles delete events for MutableDict."""

        dict.__delitem__(self, key)
        self.changed()

    def __getstate__(self):
        """
        Return dictionary contents."""
        return dict(self)

    def __setstate__(self, state):
        """
        Reset dictionary contents."""
        self.update(state)


Base = declarative_base()


class User(db.Model, Base):
    """
    Represents user table"""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    acc_status = db.Column(db.String(40), default="member")
    borrowed_books = db.Column(MutableDict.as_mutable(db.PickleType), default={})

    def __init__(self, user_info):
        """
        Sets values of a book object."""

        self.name = user_info['name']
        self.email = user_info['email']
        self.username = user_info['username']
        self.password = user_info['password']

        if 'user_id' in user_info:
            self.id = user_info['user_id']
        if 'acc_status' in user_info:
            self.acc_status = user_info['acc_status']
        if 'borrowed_books' in user_info:
            self.borrowed_books = user_info['borrowed_books']

    def add_to_reg(self):
        """
        Adds books to library dict."""
        # print(self)
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_user(param):
        """
        Fetches user details from register."""
        # print(User.query.filter(User.username == username))

        if type(param) == int:
            return User.query.filter_by(id=param).first()
        elif type(param) == str:
            return User.query.filter_by(username=param).first()

    def change_status(self, new_status):

        self.acc_status = new_status
        db.session.add(self)
        db.session.commit()

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

    def get_all_borrowed(self, order=False, order_param='return_date'):
        """
        Returns list of borrowed books by user.

        :param order: determines ordering of results. True - ascending.
        :param order_param: parameter used to order query results
        :return: borrowed_dict, record_details
        """

        # Holds temp list of borrowed_books.
        borrowed_two = []

        # Adds key and value pairs to list borrowed_two.
        for y, x in enumerate(self.borrowed_books):
            borrowed_two.append({'id': x})
            borrowed_two[y].update(self.borrowed_books[x])

        # Sorts list borrowed_two in order of descending date.
        borrowed_sorted = sorted(borrowed_two, key=lambda date: date[order_param], reverse=order)

        borrowed_dict = {}
        keys = []

        # Recreates dict a sorted according to date.
        for val in borrowed_sorted:
            borrowed_dict[val['id']] = val
            keys.append(val['id'])
            del borrowed_dict[val['id']]['id']

        return borrowed_dict, {'keys': keys, 'records': len(borrowed_dict)}

    @staticmethod
    def set_borrowed():
        """
        Provides borrow/return book functionality."""

        borrow_info = dict()

        borrow_info["borrow_date"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        borrow_info["ERD"] = (datetime.now() + timedelta(days=10)).strftime(
            "%d/%m/%Y %H:%M")
        borrow_info["ARD"] = ''
        borrow_info["fee_owed"] = 0
        borrow_info["status"] = "valid"

        return borrow_info

    def add_to_borrowed(self, book_id, borrow_info):
        """
        Adds borrowed book to borrowed_books dictionary."""

        self.borrowed_books[book_id] = borrow_info
        db.session.commit()

    def update_borrowed(self, book_id, borrow_period, get=False):
        """
        Updates borrowed book info."""

        borrowed = self.borrowed_books[book_id]
        if borrow_period > 0:
            borrowed["fee_owed"] = borrow_period * 30
            self.add_to_borrowed(book_id, borrowed)

        if not get:
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


class UserLog(db.Model):
    """
    Represent book log object."""

    __tablename__ = "user_logs"

    log_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    action = db.Column(db.String(30), nullable=False)
    success = db.Column(db.Boolean)

    def __init__(self, user_id, action='INSERT', success=True):
        """
        Initialize BookLog object."""

        self.user_id = user_id
        self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.action = action
        self.success = success

    def add_to_log(self):
        """
        Save created log entry to BookLog."""

        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_logs(*user_id):
        """
        Gets all entries in log."""

        if user_id:
            return UserLog.query.filter_by(user_id=user_id).all()
        else:
            return UserLog.query.all()

    def __repr__(self):
        """
        Represents the object instance of the model when queried."""
        return str({
            self.log_id: {
                "book_id": self.user_id,
                "timestamp": self.timestamp,
                "action": self.action,
                "success": self.success
            }
        })
