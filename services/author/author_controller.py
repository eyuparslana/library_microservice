from datetime import datetime
from flask import Flask
from flask import request
from flask_expects_json import expects_json
from flask_api import status as response_status
import utils
from services.author.author_model import AuthorModel
from services.author import author_service

app = Flask(__name__)

schema = {
    'type': 'object',
    'properties': {
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'birth_date': {'type': 'string'},
    },
    'required': ['first_name', 'last_name', 'birth_date']
}


@app.route("/author", methods=['POST'])
@expects_json(schema)
def add_author():
    token = request.headers.get('auth_token')
    token_is_exist = author_service.check_token(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    request_data = request.json
    first_name = request_data['first_name']
    last_name = request_data['last_name']
    birth_date = datetime.strptime(request_data['birth_date'], '%d/%m/%Y')

    author = AuthorModel(first_name, last_name, birth_date)

    message, is_created = author_service.add_author(author)
    status = response_status.HTTP_201_CREATED
    if not is_created:
        status = response_status.HTTP_409_CONFLICT
    return message, status


@app.route('/author/<author_id>', methods=['PUT'])
@expects_json(schema)
def update_author(author_id):
    token = request.headers.get('auth_token')
    token_is_exist = author_service.check_token(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    update_data = request.get_json(force=True)
    first_name = update_data['first_name']
    last_name = update_data['last_name']
    birth_date = datetime.strptime(update_data['birth_date'], '%d/%m/%Y')

    author = AuthorModel(first_name, last_name, birth_date)
    message, is_updated = author_service.update_author(author, author_id)
    status = response_status.HTTP_200_OK
    if not is_updated:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


@app.route('/author/<author_id>', methods=['DELETE'])
def delete_author(author_id):
    token = request.headers.get('auth_token')
    token_is_exist = author_service.check_token(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    message, is_deleted = author_service.delete_author(author_id)
    status = response_status.HTTP_200_OK
    if not is_deleted:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


@app.route('/author/<author_id>', methods=['GET'])
def get_author_by_id(author_id):
    token = request.headers.get('auth_token')
    token_is_exist = author_service.check_token(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    message, is_exist = author_service.get_author_by_id(author_id)
    status = response_status.HTTP_200_OK
    if not is_exist:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


@app.route('/author', methods=['GET'])
def get_all_author():
    token = request.headers.get('auth_token')
    token_is_exist = author_service.check_token(token)
    if not token_is_exist:
        return {'status': 'Error',
                'message': 'Token is not found or token timed out. Login again'}, response_status.HTTP_404_NOT_FOUND

    message, is_exist = author_service.get_all_author()
    status = response_status.HTTP_200_OK
    if not is_exist:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


if __name__ == '__main__':
    app, mongo = utils.config(app)
    app.run(host='localhost', port=5002)
