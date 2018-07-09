"""
Endpoint user models."""

from app import db
from datetime import datetime

from passlib.hash import sha256_crypt


class User(db.Model):
    """Represent user table"""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    acc_status = db.Column(db.String(40), default="member")
    books = db.relationship('Book', secondary='borrowed_books')

    def __init__(self, user_info):
        """
        Sets values of a book object.

        :param user_info: dict containing details of user to be added to to users table
        :type user_info: dict
        """

        self.name = user_info['name']
        self.email = user_info['email']
        self.username = user_info['username']
        self.password = sha256_crypt.encrypt(user_info['password'])

        if 'user_id' in user_info:
            self.id = user_info['user_id']
        if 'acc_status' in user_info:
            self.acc_status = user_info['acc_status']

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

    @staticmethod
    def get_email(param):
        """
        Check if email already in use.

        :param param: provided email
        :type param: string
        :return: status of email present
        :rtpye: bool
        """

        if User.query.filter_by(email=param).first():
            return True

    def change_status(self, new_status):
        """
        Change user status.

        :param new_status: new user status/role
        :type new_status: str
        """

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
            return None

    def __repr__(self):
        """
        Represent the object instance of the model when queried.

        :return: list of user object details
        :rtype: list
        """
        return {
                "user_id": self.id,
                "name": self.name,
                "password": self.password,
                "username": self.username,
                "email": self.email,
                "acc_status": self.acc_status
        }


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
        return {
            self.log_id: {
                "book_id": self.user_id,
                "timestamp": self.timestamp,
                "action": self.action,
                "success": self.success
            }
        }
