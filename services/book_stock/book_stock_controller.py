from flask import Flask, request
from services.book_stock import book_stock_service
from flask_api import status as response_status
from services.book_stock.book_stock_model import BookStockModel

app = Flask(__name__)


@app.route('/stock', methods=['POST'])
def add_stock():
    token = request.headers.get('auth_token')
    token_is_exist = book_stock_service.token_check(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    request_data = request.get_json(force=True)
    book_id = request_data.get('book_id')
    count = request_data.get('count') if request_data.get('count') else 1

    stock = BookStockModel(book_id, count)
    message, is_created = book_stock_service.create_stock(stock)
    status = response_status.HTTP_200_OK
    if is_created:
        status = response_status.HTTP_409_CONFLICT
    return message, status


@app.route('/stock/<book_id>', methods=['PUT'])
def update_stock(book_id):
    token = request.headers.get('auth_token')
    token_is_exist = book_stock_service.token_check(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    request_data = request.get_json(force=True)
    count = request_data.get('count')

    message, is_updated = book_stock_service.update_stock(book_id, count)
    status = response_status.HTTP_200_OK
    if is_updated:
        status = response_status.HTTP_409_CONFLICT
    return message, status


@app.route('/stock/<book_id>', methods=['GET'])
def get_stock_by_id(book_id):
    token = request.headers.get('auth_token')
    token_is_exist = book_stock_service.token_check(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    message, is_exist = book_stock_service.get_stock_by_id(book_id)
    status = response_status.HTTP_200_OK
    if not is_exist:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


@app.route('/stock/', methods=['GET'])
def get_all_book_stock():
    token = request.headers.get('auth_token')
    token_is_exist = book_stock_service.token_check(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    message, is_exist = book_stock_service.get_all_book_stock()
    status = response_status.HTTP_200_OK
    if not is_exist:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


if __name__ == '__main__':
    app.run(host='localhost', port=5005)
