import json
import logging
import jsonify
import requests
from bson.objectid import ObjectId

import utils
from services.user.user_controller import app

app, mongo = utils.config(app)


def register(user):
    if is_exists(user.username):
        return {'status': 'Error', 'message': 'User Already Exists!'}, False

    save(user)
    return {'status': 'Success', 'message': 'User Created!'}, True


def login(user):
    if not is_exists(user.username):
        return {'status': 'Error', 'message': 'User is not exists!'}, False

    token_add_url = utils.TOKEN_SERVICE_URL + '/add_token'
    user_id = get_user_id(user.username)

    token_add_response = requests.get(token_add_url, params={'user_id': user_id})
    token_json = token_add_response.json()

    return {'status': 'Success', 'message': 'Login Successful', 'token': token_json['token']}, True


def is_exists(username):
    row = mongo.users.find_one({'username': username})
    if row:
        return True
    return False


def get_user_id(username):
    row = mongo.users.find_one({'username': username})
    return row['_id']


def save(user):
    _id = mongo.users.insert(user.__dict__)
    logging.debug('User Created: ', user.username)
    logging.debug('User ID: ', _id)


def update(user, user_id):
    user_is_exist = mongo.users.find_one({"_id": ObjectId(user_id)})
    if not user_is_exist:
        return {"status": "Error", "message": "User not found!"}, False
    mongo.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"username": user.username, "password": user.password}})
    return {"status": "Success", "message": "User update has been successful."}, True


def delete(user_id):
    user_is_exist = mongo.users.find_one({"_id": ObjectId(user_id)})
    if not user_is_exist:
        return {"status": "Error", "message": "User not found!"}, False
    mongo.users.delete_one({"_id": ObjectId(user_id)})
    return {"status": "Success", "message": "User delete has been successful."}, True


def get_user_by_id(user_id):
    user_is_exist = mongo.users.find_one({"_id": ObjectId(user_id)})
    if not user_is_exist:
        return {"status": "Error", "message": "User not found!"}, False
    user = mongo.users.find_one({"_id": ObjectId(user_id)})
    return {"status": "Success", "result": utils.result_serializer(user)}, True


def get_all_users():
    users = mongo.users.find()
    return {"status": "Success", "result": utils.result_serializer(list(users))}, True
