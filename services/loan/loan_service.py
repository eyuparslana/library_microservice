from datetime import datetime
import requests
from bson import ObjectId
from flask_api import status as response_status
import utils
import jwt
from services.loan.loan_controller import app

app, mongo = utils.config(app)


def token_check(token):
    url = utils.TOKEN_SERVICE_URL + '/check_token/' + token

    token_service_response = requests.get(url)
    if token_service_response.status_code == response_status.HTTP_200_OK:
        return token
    return False


def get_user_id_from_token(token):
    decoded_token = jwt.decode(token.encode(), utils.SECRET_KEY, algorithms=utils.JWT_ALGORITHM)
    return decoded_token['user_id']


def add_loan(loan, token):
    headers = {'auth_token': token}
    url = utils.BOOK_STOCK_SERVICE_URL + "/book/" + loan.book_id
    data = {'book_id': loan.book_id, 'count': -1}
    book_check_response = requests.put(url, data=data, headers=headers)
    if book_check_response.status_code == response_status.HTTP_404_NOT_FOUND:
        return {'status': 'Error', 'message': 'Invalid Book ID'}, False

    loan.loaned_by = get_user_id_from_token(token)
    now = datetime.now()
    loan.due_date = now.replace(day=now.day+15).strftime("%d/%m/%Y")

    _id = mongo.loans.insert(loan.__dict__)
    return {'status': 'Success', 'message': 'Loan Success'}, True


def update_loan(loan_id, book_id):
    loan = mongo.loans.find_one({'_id': ObjectId(loan_id)})
    if not loan:
        return {'status': 'Error', 'message': 'Loan info not found'}, False

    _id = mongo.loans.update_one({'_id': ObjectId(loan_id)}, {'$set': {'book_id': book_id}})
    return {'status': 'Success', 'message': 'Loan Updated'}, False


def delete_loan(loan_id):
    loan = mongo.loans.find_one({'_id': ObjectId(loan_id)})
    if not loan:
        return {'status': 'Error', 'message': 'Loan info not found'}, False

    _id = mongo.loans.delete_one({'_id': ObjectId(loan_id)})
    return {'status': 'Success', 'message': 'Loan Deleted!'}, True


def get_loan_by_id(loan_id):
    loan = mongo.loans.find({'_id': ObjectId(loan_id)})
    tmp_loan = loan
    if not tmp_loan:
        return {'status': 'Error', 'message': 'Loan info not found'}, False
    return {'status': 'Error', 'result': utils.result_serializer(tmp_loan)}, True


def get_loans():
    loan = mongo.loans.find()
    tmp_loan = list(loan)
    if not tmp_loan:
        return {'status': 'Error', 'message': 'Loan info not found'}, False
    return {'status': 'Error', 'result': utils.result_serializer(tmp_loan)}, True
