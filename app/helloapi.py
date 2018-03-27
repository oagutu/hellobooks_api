'''holds api endpoints'''

from flask import Flask, request, jsonify

from app import create_app

app = create_app('development')

class Book(object):
    '''holds book objects'''

    def __init__(self):
        self.id = None
        self.title = None
        self.code = None
        self.author = None
        self. synopsis = None
        self.genre = None
        self.sub_genre = None
        self.status = None
        self.library = {}
    
    def add_to_lib(self, key, book_details):
        '''adds books to library dict'''
        self.library[key] = book_details
    
    def get_all_books(self):
        
        return self.library
        


value_list = ['bk_id', 'title', 'code', 'author', 'synopsis'
    'genre', 'sub_genre', 'status']

book = Book()
    

@app.route('/api/books', methods= ['POST'])
def add_book():
    '''adds book to library'''
   
    if request.method == "POST":

        r = request.get_json()
        book.bk_id = r.get('bk_id')
        book.title = r.get('title')
        book.code = r.get('code')
        book.author = r.get('author')
        book.synopsis = r.get('synopsis')
        book.genre = r.get('genre')
        book.sub_genre = r.get('sub_genre')
        book.status = r.get('status')

        if r:
            resp = jsonify({
                'bk_id' : book.bk_id,
                'title' : book.title,
                'code' : book.code,
                'author' : book.author,
                'synopsis' : book.synopsis,
                'genre' : book.genre,
                'sub_genre' : book.sub_genre,
                'status' : book.status
            }
            )
            book.add_to_lib(book.bk_id, resp.data)
            #adds new book entry to lib
            resp.status_code = 201

            return resp


@app.route('/api/books/<int:bk_id>', methods=['PUT'])
def update_book():

    if request.method == "PUT":
        
        r = request.get_json()
        temp_r = {}
        
        for val in value_list:
            if r.get(val) in r:
                book.val = r.get(val)
                temp_r[val] = book.val
        resp = jsonify(temp_r)
        
        return resp


@app.route('/api/books/<int:bk_id>', methods=['DELETE'])
def remove_book():
    
    if request.method == 'DELETE':
        r = request.get_json()
        book.bk_id = r.get('bk_id')
        del book.library[book.bk_id]

        resp = jsonify({'bk_id': book.bk_id,
                       'title': book.title, })
        
        resp.msg = 'Book entry deleted'
        
        return resp


@app.route('api/books', methods=['GET'])
def retrieve_all_books():
    '''retieves all books in library'''

    if request.method == 'GET':

        for book in book.get_all_books():
            resp = jsonify(book)
        resp.status_code = 200

        return resp
    


@app.route('/api/books/<int:id>', methods=['GET'])
def get_book():
    '''gets specific book'''

    if request.method == 'GET':
        r = request.get_json()
        book.book_id = r.get('bk_id')
        
        if r:
            for bk in book.get_all_books():
                if bk['bk_id'] == book.book_id:
                    resp = jsonify(bk)

                    resp.status_code = 200

                    return resp


@app.route('/api/users/books/<int:id>', methods=['POST'])
def borrow_return_book():
    '''allows borrowing/returning of books'''

    if request.method == 'POST':
        r = request.get_json()
        book.book_id = r.get('bk_id')

        for bk in book.get_all_books():
            if bk['bk_id'] == book.book_id and bk['status'] == 'available':
                bk['status'] = 'borrowed'
                resp = jsonify(bk)

                return resp
                
            bk['status'] = 'returned'
            resp = jsonify(bk)

            return resp
