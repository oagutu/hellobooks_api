""""
app/blacklist/models.py
Blacklist model. Holds invalid tokens.
"""

from app import db
from datetime import datetime


class Blacklist(db.Model):
    """
    Represents token blacklist obj
    """

    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        """
        Set token index value and datetime info

        :param token: access token to be revoked
        :type token: str
        """
        self.token = token
        self.time = datetime.now()

    def add_to_blacklist(self):
        """Save blacklist instance to db."""

        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_token(token):
        """Fetch specified token"""

        return Blacklist.query.filter_by(token=token).first()

    def __repr__(self):
        """Represents queried token obj"""

        return str({
            "token_index": self.token
        })
