"""
app/books/models.py
endpoint books models
"""
import enum
from app import db
from datetime import datetime


class Genre(enum.Enum):
    """Represent genre enum object data type."""

    Fiction = "fiction"
    Non_fiction = "non-fiction"


class Book(db.Model):
    """Represent book table."""

    __tablename__ = "books"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_code = db.Column(db.BIGINT, unique=True, nullable=False)
    title = db.Column(db.String(60))
    ddc_code = db.Column(db.String(30))
    author = db.Column(db.String(50))
    synopsis = db.Column(db.Text, nullable=True)
    genre = db.Column(db.Enum(Genre))
    sub_genre = db.Column(db.String(70), nullable=True, default="NA")
    status = db.Column(db.String(50), default="available", nullable=False)

    def __init__(self, book_info):
        """
        Initialize book object.

        :param book_info: dict containing details of book to be added to books table
        :type book_info: dict
        """

        self.title = book_info['title']
        self.book_code = book_info['book_code']
        self.ddc_code = book_info['ddc_code']
        self.author = book_info['author']
        self.genre = book_info['genre']

        if 'book_id' in book_info:
            self.id = book_info['book_id']
        if 'synopsis' in book_info:
            self. synopsis = book_info['synopsis']
        if 'sub_genre' in book_info:
            self.sub_genre = book_info['sub_genre']
        if 'status' in book_info:
            self.status = book_info['status']

    def add_to_lib(self):
        """Add books to library table."""

        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_book(param):
        """
        Return specified book by book_id, book_code or title.

        :param param: represents search parameter used to get book. Either book_code, id or title.
        :type param: int or str
        :return: list object containing single specified book.
        """

        if type(param) == int and len(str(param)) == 12:
            return Book.query.filter_by(book_code=param).first()
        elif type(param) == int:
            return Book.query.filter_by(id=param).first()
        else:
            return Book.query.filter_by(title=param).all()

    @staticmethod
    def get_all_books(entries=3, page=1):
        """
         Return all books in library.

        :param entries: specifies number of query results to be returned.
        :type entries int
        :param page: specifies page necessary fpr pagination of returned results.
        :type page: int
        :return: list object containing all books in the library
        :rtype: list
        """

        return Book.query.paginate(page, entries, True).items

    def delete_book(self):
        """Delete specific book entry from books_table."""

        db.session.delete(self)
        db.session.commit()

    def set_book_status(self, status):
        """Set the status of the book after borrowing/returning."""

        self.status = status
        db.session.commit()

    def __repr__(self):
        """
        Return the object instance of the model when queried.

        :return: list of queried book objects
        """

        return str({
            self.id: {
                "title": self.title,
                "author": self.author,
                "genre": self.genre,
                "sub_genre": self.sub_genre,
                "synopsis": self.synopsis,
                "book_code": self.book_code,
                "ddc_code": self.ddc_code,
                "status": self.status
            }
        })


class BookLog(db.Model):
    """Represent book log object."""

    __tablename__ = "book_logs"

    log_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    action = db.Column(db.String(30), nullable=False)
    success = db.Column(db.Boolean)

    def __init__(self, book_id, action='INSERT', success=True):
        """
        Initialize BookLog object.

        :param book_id: id of book object to be acted on
        :type book_id: int
        :param action: type of acton performed on book object
        :type action: str
        :param success: status of action to be committed on book object
        :type success: bool
        """

        self.book_id = book_id
        self.timestamp = datetime.now().strftime("%m/%d/%Y %H:%M")
        self.action = action
        self.success = success

    def add_to_log(self):
        """Save created log entry to BookLog."""

        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_logs(*book_id):
        """
        Return all entries in book_logs.
        
        :param book_id: used to get logs for specific book
        :type book_id: int
        :return: List object containing query results
        :rtype: list
        """

        if book_id:
            return BookLog.query.filter_by(book_id=book_id).all()
        else:
            return BookLog.query.all()

    def __repr__(self):
        """
        Represent the object instance of the model when queried.

        :return: list of que=ried book objects
        """
        
        return str({
            self.log_id: {
                "book_id": self.book_id,
                "timestamp": self.timestamp,
                "action": self.action,
                "success": self.success
            }
        })
