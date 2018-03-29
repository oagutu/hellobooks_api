'''endpoint models'''

class Book(object):
    '''holds book objects'''

    def __init__(self):
        self.bk_id = None
        self.title = None
        self.code = None
        self.author = None
        self. synopsis = None
        self.genre = None
        self.sub_genre = None
        self.status = None
        self.library = {}

    def set_book(self, book_id, title, author):
        '''sets value of a book object'''
        
        self.book_id = book_id
        self.title = title
        self.author = author

        book_details = {
            "book_id" : self.book_id,
            "title" : self.title,
            "author" : self.author,}

        return book_details

    def add_to_lib(self, key, book_details):
        '''adds books to library dict'''
        self.library[key] = book_details

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
