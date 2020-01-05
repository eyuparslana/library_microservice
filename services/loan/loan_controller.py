from flask import Flask, request
from services.loan import loan_service
from flask_api import status as response_status
from flask_expects_json import expects_json

from services.loan.loan_model import LoanModel

app = Flask(__name__)

schema = {
    'type': 'object',
    'properties': {
        'book_id': {'type': 'string'},
    },
    'required': ['book_id']
}


@app.route('/loan', methods=['POST'])
def create_loan():
    token = request.headers.get('auth_token')
    token_is_exist = loan_service.token_check(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    request_data = request.get_json(force=True)
    book_id = request_data['book_id']
    loan = LoanModel(book_id=book_id)
    message, is_created = loan_service.add_loan(loan, token)
    status = response_status.HTTP_200_OK
    if not is_created:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


@app.route('/loan/<loan_id>', methods=['PUT'])
def update_loan(loan_id):
    token = request.headers.get('auth_token')
    token_is_exist = loan_service.token_check(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    request_data = request.get_json(force=True)
    book_id = request_data['book_id']
    message, is_updated = loan_service.update_loan(loan_id, book_id)
    status = response_status.HTTP_200_OK
    if not is_updated:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


@app.route('/loan/<loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    token = request.headers.get('auth_token')
    token_is_exist = loan_service.token_check(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    message, is_deleted = loan_service.delete_loan(loan_id)
    status = response_status.HTTP_200_OK
    if not is_deleted:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


@app.route('/loan/<loan_id>', methods=['GET'])
def get_loan_by_id(loan_id):
    token = request.headers.get('auth_token')
    token_is_exist = loan_service.token_check(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    message, is_exist = loan_service.get_loan_by_id(loan_id)
    status = response_status.HTTP_200_OK
    if not is_exist:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


@app.route('/loan/', methods=['GET'])
def get_loans():
    token = request.headers.get('auth_token')
    token_is_exist = loan_service.token_check(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    message, is_exist = loan_service.get_loans()
    status = response_status.HTTP_200_OK
    if not is_exist:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


if __name__ == '__main__':
    app.run(host='localhost', port=5004)
