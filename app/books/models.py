"""
app/books/models.py
endpoint books models
"""


library = {
    1: {
        "book_id": 1,
        "title": "book title",
        "book_code": 12345,
        "author": "mary writer",
        "synopsis": "iwehn owueh owunef ohew ouweq...",
        "genre": "fiction",
        "sub_genre": "xyz",
        "status": "borrowed"},
    2: {
        "book_id": 2,
        "title": "Catch-22",
        "book_code": 6753,
        "author": "Heller",
        "synopsis": "iwehn owueh owunef ohew ouweq...",
        "genre": "fiction",
        "sub_genre": "xyz",
        "status": "borrowed"},
}


class Book(object):
    """
    Used to create book objects."""

    def __init__(self):
        """
        Initializes book object"""

        self.bk_id = None
        self.title = None
        self.code = None
        self.author = None
        self. synopsis = None
        self.genre = None
        self.sub_genre = None
        self.status = None

    def set_book(self, book_info):
        """
        Sets value of a book object."""

        bk_params = ["book_id", "title", "author", "book_code", "synopsis",
                     "genre", "subgenre"]
        book_details = {}

        for detail in bk_params:
            if detail in book_info:
                book_details[detail] = book_info[detail]

        book_details["status"] = "available"
        self.add_to_lib(book_details)

        return book_details

    def add_to_lib(self, book_details):
        """
        Adds books to library dict."""

        global library
        library[book_details['book_id']] = book_details

    def get_book(self, book_id):
        """
        Gets book by book_id."""

        global library
        if library[book_id]:
            return library[book_id]

    def get_all_books(self):
        """
        Gets all books in library."""

        global library
        return library
