'''endpoint models'''

from datetime import datetime, timedelta


register = {
    "John": {
        "user_id": 2334,
        "name": "John Paul",
        "username": "John",
        "email": "qwert@keyboard.com",
        "password": "1234",
        "acc_status": "member"
    }
}


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
            1 : {
            "book_id": 1,
            "title": "book title",
            "book_code": 12345,
            "author": "mary writer",
            "synopsis": "iwehn owueh owunef ohew ouweq...",
            "genre": "fiction",
            "sub_genre": "xyz",
            "status": "borrowed"}
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
    '''hold user objects'''

    
    def __init__(self):
        '''initializes user object'''
        self.user_id = None
        self.name = None
        self.username = None
        self.email = None
        self.password = None
        self.acc_status = None
        
        self.borrowed_books = {
            23:{
                "borrow_date" : "25/04/2018 02:30",
                "return_date" : "1/05/2018 02:30",
                "fee_owed" : 0,
                "borrow_status": "valid"
            }
        }

    def set_user(self, user_info):
        '''sets value of a book object'''

        user_params = ["user_id", "name", "email", "username", "password", "acc_status",
                     "borrowed_books"]
        user_details = {}

        if len(user_params) == len(user_info):

            for val, detail in enumerate(user_params):
                user_details[detail] = user_info[val]

        self.add_to_reg(user_details["username"], user_details)

        return user_details
    
    def set_password(self, user_info):
        '''
        sets user paxsword
        user_info: list -> [username, current_password, new_password]
        '''
        if register[user_info[0]]['password'] != user_info[2]:
            user_details = register[user_info[0]]
            user_details['password'] = user_info[2]
        

    def get_user(self, username):
        '''fetches user details from registrer'''
        global register
        return register[username]

    def set_borrowed(self, book_status, book_id):
        '''provdes borrow/return book functionality'''

        book_info = {}
            
        book_info["borrow_date"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        book_info["return_date"] = (datetime.now() + timedelta(days=10)).strftime(
            "%d/%m/%Y %H:%M")
        book_info["fee_owed"] = 0
        book_info["status"] = "valid"

        return book_info
            
            
    def get_borrowed(self, book_id):
        '''gets a book from the list of borrowed books by id'''
        if self.borrowed_books[book_id]:
            return self.borrowed_books[book_id]
        
    def add_to_borrowed(self, key, details):
        '''adds borrowed book to borrowed_books dictionary'''
        self.borrowed_books[key] = details

    def add_to_reg(self, key, user_details):
        '''adds books to library dict'''
        global register
        register[key] = user_details

    def get_register(self):
        '''returns all users'''
        global register

        return register
