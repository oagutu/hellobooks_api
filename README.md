# hellobooks_api
hellobooks_api
API endpoints for the Hello Books Flask web app project

## Supported API endpoints

add book: POST  /api/books

edit book: PUT /api/books/<bookId>

Remove a book: DELETE /api//books/<bookId>

Retrieves all books: GET  /api/books

Get a book : GET  /api/books/<bookId>

Borrow a book POST  /api/users/books/<bookId>

Creates a user account POST /api/auth/register

Logs in a user POST /api/auth/login

Logs out a user: POST /api/auth/logout

Password reset: POST /api/auth/reset-password




## Setup:

clone repo to local machine

Install requirement packages via 'requirements.txt': $ pip install -r requirments.txt

Run server: $ python run.py
