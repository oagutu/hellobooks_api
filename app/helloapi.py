'''holds api endpoints'''

from flask import Flask, request, jsonify

from app import create_app

app = create_app('development')

@app.route('/api/books', methods= ['POST', 'GET'])
def add_book(*payload):
    
    book = {}
    
    if request.method == "POST":

            r = request.get_json(force=True)
            book['id'] = r.get('id')
            book['title'] = r.get('title')
            book['code'] = r.get('code')
            book['author'] = r.get('author')
            book['synopsis'] = r.get('synopsis')
            book['genre'] = r.get('genre')
            book['sub-genre'] = r.get('sub-genre')
            book['status'] = r.get('status')

            print(book)

            if r:
                resp = jsonify(book)
                resp.status_code = 201

            # r = requests.post('/api/books', data=payload)
            # book = r.text

                return resp
