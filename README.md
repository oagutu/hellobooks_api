[![Build Status](https://travis-ci.org/oagutu/hellobooks_api.svg?branch=master)](https://travis-ci.org/oagutu/hellobooks_api)
[![Coverage Status](https://coveralls.io/repos/github/oagutu/hellobooks_api/badge.svg?branch=master)](https://coveralls.io/github/oagutu/hellobooks_api?branch=master)

# hellobooks_api
---
API endpoints for the Hello Books Flask web app project. It should allow for accessing of book and user information.

### Supported API endpoints:

* add book: POST  /api/v1/books

* edit book: PUT /api/v1/books/<bookId>

* Remove a book: DELETE /api/v1/books/<bookId>

* Retrieves all books: GET  /api//v1books

* Get a book : GET  /api/v1/books/<bookId>

* Borrow a book POST  /api/v1/users/books/<bookId>

* Creates a user account POST /api/v1/auth/register

* Logs in a user POST /api/v1/auth/login

* Logs out a user: POST /api/v1/auth/logout

* Password reset: POST /api/v1/auth/reset-password


## Setup:
---

* clone repo to local machine:
```
$ git clone https://github.com/oagutu/hellobooks_api
```
* Install requirement packages/ dependencies via 'requirements.txt': 
```
$ pip install -r requirments.txt
```

* Navigate to main directory and run server:
```
$ python run.py
```

## Running
---

You could use postman to test API endpoints:

* Download [postman](https://www.getpostman.com/apps)

* Send requests using Postman

For the endpoints, requests submitted using JSON. Example of JSON request:

```
{       
        "book_id": 1,
        "title": "book title",
        "book_code": 12345,
        "author": "mary writer",
        "synopsis": "Iwehn owueh owunef ohew ouweq...",
        "genre": "fiction",
        "subgenre": "xyz",
        "status": "available"
}
```

## Testing
* With nosetests, navigate to main project directory and run nosetests:
```
nosetests
```
* Without nosetests, navigate to tests directory in main project directory:
```
cd tests

python test_books.py

python test_users.py
```
