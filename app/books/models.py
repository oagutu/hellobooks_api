'''endpoint books models'''

from datetime import datetime, timedelta


class Book(object):
    '''holds book objects'''

    def __init__(self):
        '''initializes book object'''
        self.bk_id = None
        self.title = None
        self.code = None
        self.author = None
        self. synopsis = None
        self.genre = None
        self.sub_genre = None
        self.status = None
        self.library = {
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

    def set_book(self, book_info):
        '''sets value of a book object'''

        bk_params = ["book_id", "title", "author", "book_code", "synopsis",
                     "genre", "subgenre", "status"]
        book_details = {}

        if len(bk_params) == len(book_info):

            for val, detail in enumerate(bk_params):
                book_details[detail] = book_info[val]

        self.add_to_lib(book_details["book_id"], book_details)

        return book_details

    def add_to_lib(self, key, book_details):
        '''adds books to library dict'''
        self.library[key] = book_details

    def get_book(self, book_id):
        '''gets book by id'''
        if self.library[book_id]:
            return self.library[book_id]

    def get_all_books(self):

        return self.library
