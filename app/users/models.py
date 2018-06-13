"""
Endpoint user models."""

from app import db
from datetime import datetime, timedelta

from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.ext.declarative import declarative_base

from passlib.hash import sha256_crypt
# from werkzeug.security import generate_password_hash, check_password_hash


class MutableDict(Mutable, dict):
    """
    Represent MutableDict object.

    Allows for borrowed books pickle to be mutable.
    """

    @classmethod
    def coerce(cls, key, value):
        """Convert dictionary to MutableDict type."""

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        """Handle set events for MutableDict."""

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        """
        Handle delete events for MutableDict.

        :param key: dict key used to determine dict entry to be deleted
        :tyoe key: str
        """

        dict.__delitem__(self, key)
        self.changed()

    def __getstate__(self):
        """
        Return dictionary contents.

        :return: borrowed_book contents for queried book object
        :rtype: dict
        """
        return dict(self)

    def __setstate__(self, state):
        """
        Reset dictionary contents.

        :param state: state of of queried result(ie. the borrowed book entry)
        """
        self.update(state)


Base = declarative_base()


class User(db.Model, Base):
    """Represent user table"""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    acc_status = db.Column(db.String(40), default="member")
    borrowed_books = db.Column(MutableDict.as_mutable(db.PickleType), default={})

    def __init__(self, user_info):
        """
        Sets values of a book object.

        :param user_info: dict containing details of user to be added to to users table
        :type user_info: dict
        """

        self.name = user_info['name']
        self.email = user_info['email']
        self.username = user_info['username']
        # hash_password = sha256_crypt.encrypt(user_info['password'])
        # self.password = generate_password_hash(user_info['password'])
        # self.password = user_info['pas']
        self.password = sha256_crypt.encrypt(user_info['password'])

        if 'user_id' in user_info:
            self.id = user_info['user_id']
        if 'acc_status' in user_info:
            self.acc_status = user_info['acc_status']
        if 'borrowed_books' in user_info:
            self.borrowed_books = user_info['borrowed_books']

    def add_to_reg(self):
        """Add books to library dict."""

        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_user(param):
        """
        Fetch user details from register.

        :param param: parameter used to search for specific user object
        :type param: int or str
        :return:  query obj for specified user
        :rtype: query obj
        """
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
        Return all users.

        :return: query object with a;l users
        :rtype: query obj
        """

        return User.query.all()

    def set_password(self, user_info):
        """
        Sets user password.

        :param user_info: dict holding username, current_password & new password
        :type user_info: dict
        """

        if sha256_crypt.verify(user_info[1], self.password):
            self.password = sha256_crypt.encrypt(user_info[2])

    @staticmethod
    def verify_pass(username, password):
        """
        Verifies that password entered and in DB are equal

        :param username: username used to login
        :type username: str
        :param password: password used to login
        :type password: str
        :return: status of verification
        :rtype: boolean
        """

        user = User.get_user(username)

        if sha256_crypt.verify(password, user.password):
            return True
        else:
            return False

    def get_all_borrowed(self, order=False, order_param='return_date'):
        """
        Returns list of borrowed books by user.

        :param order: determines ordering of results. True - ascending.
        :type order: bool
        :param order_param: parameter used to order query results
        :type order_param: str
        :return: borrowed_dict, record_details
        :rtype: tuple
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
        Provides borrow/return book functionality.

        :return: info on borrowed book
        :rtype: dict
        """

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
        Add borrowed book to borrowed_books dictionary.

        :param book_id: id of book to be borrowed
        :type book_id: str
        :param borrow_info: borrow transaction details
        :type borrow_info: dict
        """

        self.borrowed_books[book_id] = borrow_info
        db.session.commit()

    def update_borrowed(self, book_id, borrow_period, get=False):
        """
        Update borrowed book info.

        :param book_id: id of borroowed book
        :type book_id: str
        :param borrow_period: no. of days book borrowed for
        :type borrow_period: int
        :param get: determines action, ie. if borrowing book or fetching borrow history
        :type get: bool
        """

        borrowed = self.borrowed_books[book_id]
        if borrow_period > 0:
            borrowed["fee_owed"] = borrow_period * 30
            self.add_to_borrowed(book_id, borrowed)

        if not get:
            self.borrowed_books[book_id]["status"] = "returned"
        db.session.commit()

    def __repr__(self):
        """
        Represent the object instance of the model when queried.

        :return: list of user object details
        :rtype: list
        """
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
    """Represent book log object."""

    __tablename__ = "user_logs"

    log_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    action = db.Column(db.String(30), nullable=False)
    success = db.Column(db.Boolean)

    def __init__(self, user_id, action='INSERT', success=True):
        """
        Initialize BookLog object.

        :param user_id: id of user object acted on
        :type user_id: int
        :param action: action performed on the user object
        :type action: str
        :param success: status of action performed on user object
        :type success: bool
        """

        self.user_id = user_id
        self.timestamp = datetime.now().strftime("%m/%d/%Y %H:%M")
        self.action = action
        self.success = success

    def add_to_log(self):
        """Save created log entry to BookLog."""

        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_logs(*user_id):
        """
        Get all entries in log.

        :param user_id: used to fetch logs for specific user
        :type: int
        :return: user logs
        :rtype: query obj
        """

        if user_id:
            return UserLog.query.filter_by(user_id=user_id).all()
        else:
            return UserLog.query.all()

    def __repr__(self):
        """
         Represent the object instance of the model when queried.

        :return: list of user log objects
        :rtype: list
        """
        return str({
            self.log_id: {
                "book_id": self.user_id,
                "timestamp": self.timestamp,
                "action": self.action,
                "success": self.success
            }
        })
