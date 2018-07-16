[![Build Status](https://travis-ci.org/oagutu/hellobooks_api.svg?branch=master)](https://travis-ci.org/oagutu/hellobooks_api)
[![Coverage Status](https://coveralls.io/repos/github/oagutu/hellobooks_api/badge.svg?branch=master)](https://coveralls.io/github/oagutu/hellobooks_api?branch=master)
<a href="https://codeclimate.com/github/oagutu/hellobooks_api/maintainability"><img src="https://api.codeclimate.com/v1/badges/d739292061baca100c02/maintainability" /></a>

# hellobooks_api

API endpoints for the Hello Books Flask web app project.
It aims to aid in user and book management in a library context.

This API can be accessed at the following url:

https://fast-stream-12738.herokuapp.com

### Supported API endpoints:

|Endpoint                  | Functionality              |HTTP method  |ADMIN ONLY
|--------------------------|----------------------------|-------------|----------
|/api/auth/register        |Creates a user account      |POST         |
|/api/auth/login           |Log in a user               |POST         |
|/api/auth/logout          |Log out a user              |POST         |
|/api/books                |Add a book                  |POST         |True
|/api/books/{*book_id*}    |modify a book’s information |PUT          |True
|/api/books/{*book_id*}    |Get a book by id            |GET          |
|/api/books                |Retrieves all books         |GET          |
|/api/books/{*book_id*}    |Remove a book               |DELETE       |True
|/api/users/books/{*book_id*}|Borrow a book             |POST         |
|/api/users/books/{*book_id*}|Return a book             |PUT          |
|/api/users/books          |Borrow history              |GET          |
|/api/auth/reset-password  |Password reset              |POST         |
|/api/auth/users/status_change|Change user status       |POST         |True
|api/v1/books/search{?q}   |Search book                 |POST         |
|api/v1/users/books/logs   |Get book logs               |POST         |True
|api/v1/auth/users/logs    |Get user logs               |POST         |True



## Setup:

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

You could use postman to test API endpoints:

* Download [postman](https://www.getpostman.com/apps)

* Send requests using Postman

For the endpoints, requests submitted using JSON. 

Example of JSON requests include:

* Create user account:

```
{
    "name": "your_name",
    "username": "your_username",
    "password": "your_password",
    "email": "your_email_address"
}  
```

* login:

```
{
	"username": "your_username",
	"password": "your password"
}
```

* add book:

```
{
    "title": "levels",
    "book_code": 941113109871,
    "ddc_code": "321.15",
    "author": "Avi K.",
    "synopsis": "I ind hwbej jb. Kesse jnew ohew ouweq...",
    "genre": "fiction",
    "sub_genre": "drama"
}
```

## Testing

* With nosetests`(recommended)`, navigate to main project directory and run nosetests:
```
nosetests
```
* Without nosetests, navigate to *tests/test_books* or *tests/test_users* directories
 in main project directory and run individual test suites:
  
  For example:
  
```
cd tests/test_books

python test_add_book.py
python test_get_books.py
python test_remove_book.py

cd tests/test_users

python test_crete_user.py
python test_login.py
python test_logout.py

```
