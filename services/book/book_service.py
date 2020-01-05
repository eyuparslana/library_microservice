import requests
from bson import ObjectId
from flask_api import status as response_status

import utils
from services.book.book_controller import app

app, mongo = utils.config(app)


def token_check(token):
    url = utils.TOKEN_SERVICE_URL + '/check_token/' + token

    token_service_response = requests.get(url)
    if token_service_response.status_code == response_status.HTTP_200_OK:
        return True
    return False


def book_exist(isbn):
    book = mongo.books.find_one({'isbn': isbn})
    if book:
        return True
    return False


def check_author(author_id, token):
    url = utils.AUTHOR_SERVICE_URL + '/author/' + author_id
    headers = {'auth_token': token}
    author_check_response = requests.get(url, headers=headers)
    if author_check_response.status_code == 200:
        return True
    return False


def add_book(book, token):
    if book_exist(book.isbn):
        return {'status': 'Error', 'message': 'Book already exist'}, False

    is_author_exist = check_author(book.author, token)
    if not is_author_exist:
        return {'status': 'Error', 'message': 'Invalid Author'}, False

    _id = mongo.books.insert(book.__dict__)
    return {'status': 'Success', 'message': 'Book Created'}, True


def check_book_by_id(book_id):
    book = mongo.books.find_one({'_id': ObjectId(book_id)})
    if book:
        return True
    return False


def update_book(book_id, book):
    if not check_book_by_id(book_id):
        return {'status': 'Error', 'message': 'Book not exist'}, False

    _id = mongo.books.update_one({'_id': ObjectId(book_id)}, {'$set': book.__dict__})
    return {'status': 'Success', 'message': 'Book Updated!'}, True


def delete_book(book_id):
    if not check_book_by_id(book_id):
        return {'status': 'Error', 'message': 'Book not exist'}, False

    _id = mongo.books.delete_one({'_id': ObjectId(book_id)})
    return {'status': 'Success', 'message': 'Book Deleted!'}, True


def get_book_by_id(book_id):
    if not check_book_by_id(book_id):
        return {'status': 'Error', 'message': 'Book not exist'}, False
    book = mongo.books.find_one({'_id': ObjectId(book_id)})
    return {'status': 'Success', 'result': utils.result_serializer(book)}, True


def get_all_books():
    books = mongo.books.find()
    all_books = list(books)
    if not all_books:
        return {'status': 'Error', 'message': 'Book not found'}, False
    return {'status': 'Success', 'result': utils.result_serializer(all_books)}, True
