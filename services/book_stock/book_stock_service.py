import requests
from bson import ObjectId

import utils
from services.book_stock.book_stock_controller import app
from flask_api import status as response_status

app, mongo = utils.config(app)


def token_check(token):
    url = utils.TOKEN_SERVICE_URL + '/check_token/' + token

    token_service_response = requests.get(url)
    if token_service_response.status_code == response_status.HTTP_200_OK:
        return True
    return False


def create_stock(stock):
    raw_stock = mongo.stocks.find_one({'book_id': stock.book_id})
    if raw_stock:
        return {'status': 'Error', 'message': 'Book already exist. Please make request with PUT method'}, False
    _id = mongo.stocks.insert(stock.__dict__)
    return True


def delete_book_stock(book_id):
    _id = mongo.stocks.delete_one({'book_id': book_id})
    return True


def update_stock(book_id, count):
    stock = mongo.stocks.find_one({'book_id': book_id})
    book_count = stock.get('count')
    if not book_count:
        return {'status': 'Error', 'message': 'Book not found'}, False
    new_count = book_count + count
    if new_count == 0:
        delete_book_stock(book_id)
        return {'status': 'Success', 'message': 'Book Over'}, True

    mongo.stocks.update_one({'book_id': book_id}, {'$set': {'count': new_count}})
    return{'status': 'Success', 'message': 'Book Stock Updated'}, True


def get_stock_by_id(book_id):
    stock = mongo.stocks.find_one({'book_id': book_id})
    stock_result = stock
    if not stock_result:
        return {'status': 'Error', 'message': 'There is no book stock'}, False
    return {'status': 'Success', 'message': utils.result_serializer(stock_result)}, True


def get_all_book_stock():
    stock = mongo.stocks.find()
    stock_result = list(stock)
    if not stock_result:
        return {'status': 'Error', 'message': 'There is no book stock'}, False
    return {'status': 'Success', 'message': utils.result_serializer(stock_result)}, True
