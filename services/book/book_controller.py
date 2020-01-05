from datetime import datetime
from flask import Flask, request
from flask_expects_json import expects_json
from flask_api import status as response_status
from services.book.book_model import BookModel
from services.book import book_service

app = Flask(__name__)


schema = {
    'type': 'object',
    'properties': {
        'book_name': {'type': 'string'},
        'isbn': {'type': 'string'},
        'publish_date': {'type': 'string'},
        'genre': {'type': 'string'},
        'author': {'type': 'string'},
    },
    'required': ['book_name', 'isbn', 'author']
}


@app.route('/book', methods=['POST'])
@expects_json(schema)
def add_book():
    token = request.headers.get('auth_token')
    token_is_exist = book_service.token_check(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    add_book_data = request.get_json(force=True)

    book_name = add_book_data.get('book_name')
    isbn = add_book_data.get('isbn')
    author = add_book_data.get('author')
    publish_date = datetime.strptime(add_book_data.get('publish_date'), '%d/%m/%Y') if add_book_data.get(
        'publish_date') else None
    genres = add_book_data.get('genres').split(',') if add_book_data.get('genres') else None

    book = BookModel(book_name, isbn, author, publish_date, genres)

    message, is_created = book_service.add_book(book, token)
    status = response_status.HTTP_200_OK
    if not is_created:
        status = response_status.HTTP_409_CONFLICT
    return message, status


@app.route('/book/<book_id>', methods=['PUT'])
@expects_json(schema)
def update_book(book_id):
    token = request.headers.get('auth_token')
    token_is_exist = book_service.token_check(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND
    update_book_data = request.get_json(force=True)
    book_name = update_book_data.get('book_name')
    isbn = update_book_data.get('isbn')
    author = update_book_data.get('author')
    publish_date = datetime.strptime(update_book_data.get('publish_date'), '%d/%m/%Y') if update_book_data.get(
        'publish_date') else None
    genres = update_book_data.get('genres').split(',') if update_book_data.get('genres') else None
    book = BookModel(book_name, isbn, author, publish_date, genres)
    message, is_updated = book_service.update_book(book_id, book)
    status = response_status.HTTP_200_OK
    if not is_updated:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


@app.route('/book/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    token = request.headers.get('auth_token')
    token_is_exist = book_service.token_check(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    message, is_deleted = book_service.delete_book(book_id)
    status = response_status.HTTP_200_OK
    if not is_deleted:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


@app.route('/book/<book_id>', methods=['GET'])
def get_book_by_id(book_id):
    token = request.headers.get('auth_token')
    token_is_exist = book_service.token_check(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    message, is_exist = book_service.get_book_by_id(book_id)
    status = response_status.HTTP_200_OK
    if not is_exist:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


@app.route('/book', methods=['GET'])
def get_all_books():
    token = request.headers.get('auth_token')
    token_is_exist = book_service.token_check(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    message, is_exist = book_service.get_all_books()
    status = response_status.HTTP_200_OK
    if not is_exist:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


if __name__ == '__main__':
    app.run(host='localhost', port=5003)
