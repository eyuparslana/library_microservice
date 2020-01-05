import requests
from bson import ObjectId
from flask_api import status as response_status
import utils
from services.author.author_controller import app

app, mongo = utils.config(app)


def check_token(token):
    url = utils.TOKEN_SERVICE_URL + "/check_token/" + token

    token_is_exist_response = requests.get(url)
    if token_is_exist_response.status_code == response_status.HTTP_200_OK:
        return True
    return False


def author_exists(first_name, last_name):
    author = mongo.authors.find_one({'first_name': first_name, 'last_name': last_name})
    if author:
        return author
    return False


def add_author(author):
    if author_exists(author.first_name, author.last_name):
        return {'status': 'Error', 'message': 'Author already exist'}, False

    _id = mongo.authors.insert(author.__dict__)
    return {'status': 'Success', 'message': 'Author Created'}, True


def check_author_by_id(author_id):
    author = mongo.authors.find_one({'_id': ObjectId(author_id)})
    if author:
        return True
    return False


def update_author(author, author_id):
    if not check_author_by_id(author_id):
        return {'status': 'Error', 'message': 'Author Not Found'}, False

    _id = mongo.authors.update_one({'_id': ObjectId(author_id)}, {
        '$set': {'first_name': author.first_name, 'last_name': author.last_name, 'birth_date': author.birth_date}})
    return {'status': 'Success', 'message': 'Author Updated!'}, True


def delete_author(author_id):
    if not check_author_by_id(author_id):
        return {'status': 'Error', 'message': 'Author Not Found'}, False

    _id = mongo.authors.delete_one({'_id': ObjectId(author_id)})
    return {'status': 'Success', 'message': 'Author Deleted!'}, True


def get_author_by_id(author_id):
    if not check_author_by_id(author_id):
        return {'status': 'Error', 'message': 'Author Not Found'}, False

    author = mongo.authors.find_one({'_id': ObjectId(author_id)})
    return {'status': 'Success', 'result': utils.result_serializer(author)}, True


def get_all_author():
    authors = mongo.authors.find()
    result = list(authors)
    if not result:
        return {'status': 'Error', 'message': 'There is no any author data'}, False
    return {'status': 'Success', 'result': utils.result_serializer(result)}, True
