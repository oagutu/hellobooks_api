"""
app/books/models.py
endpoint books models
"""

from app import db, create_app


class Book(db.Model):
    """
    Represents book table."""

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(60), nullable=False)
    book_code = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String(60), nullable=False)
    synopsis = db.Column(db.String(200), default=" ")
    genre = db.Column(db.String(50), nullable=False)
    subgenre = db.Column(db.String(50), default="NA")
    status = db.Column(db.String(40), default="available")

    def save(self, book):
        """
        Adds book to database"""

        db.session.add(book)
        db.session.commit()



# library = {
#     1: {
#         "book_id": 1,
#         "title": "book title",
#         "book_code": 12345,
#         "author": "mary writer",
#         "synopsis": "iwehn owueh owunef ohew ouweq...",
#         "genre": "fiction",
#         "sub_genre": "xyz",
#         "status": "borrowed"},
#     2: {
#         "book_id": 2,
#         "title": "Catch-22",
#         "book_code": 6753,
#         "author": "Heller",
#         "synopsis": "iwehn owueh owunef ohew ouweq...",
#         "genre": "fiction",
#         "sub_genre": "xyz",
#         "status": "borrowed"},
# }


# class Book(object):
#     """
#     Used to create book objects."""

#     def __init__(self):
#         """
#         Initializes book object"""

#         self.bk_id = None
#         self.title = None
#         self.code = None
#         self.author = None
#         self. synopsis = None
#         self.genre = None
#         self.sub_genre = None
#         self.status = None

#     def set_book(self, book_info):
#         """
#         Sets value of a book object."""

#         bk_params = ["book_id", "title", "author", "book_code", "synopsis",
#                      "genre", "subgenre", "status"]
#         book_details = {}

#         if len(bk_params) == len(book_info):

#             for val, detail in enumerate(bk_params):
#                 book_details[detail] = book_info[val]

#         self.add_to_lib(book_details)

#         return book_details


#     def add_to_lib(self, book_details):
#         """
#         Adds books to library dict."""

#         global library
#         library[book_details['book_id']] = book_details


#     def get_book(self, book_id):
#         """
#         Gets book by book_id."""

#         global library
#         if library[book_id]:
#             return library[book_id]


#     def get_all_books(self):
#         """
#         Gets all books in library."""

#         global library
#         return library
