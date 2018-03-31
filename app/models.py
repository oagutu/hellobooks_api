'''endpoint models'''

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
            23: {
            "book_id": 1,
            "title": "book title",
            "book_code": 12345,
            "author": "mary writer",
            "synopsis": "iwehn owueh owunef ohew ouweq...",
            "genre": "fiction",
            "sub_genre": "xyz",
            "status": "available"}
            }

    def set_book(self, book_info):
        '''sets value of a book object'''

        bk_params = ["book_id", "title", "author", "book_code", "synopsis",
                      "genre", "subgenre", "status"]
        book_details = {}

        if len(bk_params) == len(book_info):

            for val, detail in enumerate(bk_params):
                book_details[detail] = book_info[val]

        self.add_to_lib(book_details["book_id"] ,book_details)

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


class User(object):
    def __init__(self):
        self.uid = None
        self.name = None
        self.username = None
        self.eaddress = None
        self.password = None
        self.acc_type = None
        self.register = {}
        self.borrowed = {}

    def add_to_reg(self, key, user_details):
        '''adds books to library dict'''
        self.register[key] = user_details

    def get_all_users(self):

        return self.register
