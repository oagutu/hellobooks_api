"""
app/books/models.py
endpoint books models
"""
import enum
from app import db


class Genre(enum.Enum):
    """Represents genre enum data type"""
    Fiction = "fiction"
    Non_fiction = "non-fiction"


class Book(db.Model):
    """Represents book table"""

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
        Initializes book object"""

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
        """
        Adds books to library dict."""

        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_book(param):
        """
        Gets book by book_id."""
        if type(param) == int and len(str(param)) == 12:
            return Book.query.filter_by(book_code=param).first()
        elif type(param) == int:
            return Book.query.filter_by(id=param).first()
        else:
            return Book.query.filter_by(title=param).first()

    @staticmethod
    def get_all_books(entries=50, page=1):
        """
        Gets all books in library."""

        return Book.query.paginate(page, int(entries), True).items

    def delete_book(self):
        """
        Deletes book entries for db."""
        db.session.delete(self)
        db.session.commit()

    def set_book_status(self, status):
        """
        Sets the status of the book after borrowing/returning."""

        self.status = status
        db.session.commit()

    def __repr__(self):
        """
        Represents the object instance of the model when queried."""
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
