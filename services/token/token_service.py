import logging
from datetime import datetime
import jwt
from pymongo.errors import OperationFailure
import utils
from services.token.token_controller import app


app, mongo = utils.config(app)

try:
    mongo.tokens.ensure_index('update_time', expireAfterSeconds=24 * 3600)
except OperationFailure:
    pass


def generate_token(token):
    token.token = jwt.encode({'user_id': token.user_id, 'timestamp': datetime.now().timestamp()}, utils.SECRET_KEY,
                             algorithm=utils.JWT_ALGORITHM).decode('utf-8')
    return token


def add_token(token_obj):
    token_check = mongo.tokens.find_one({'user_id': token_obj.user_id})
    if token_check:
        now = datetime.now().utcnow()
        token_obj.token = token_check['token']
        mongo.tokens.update_one({'user_id': token_obj.user_id}, {'$set': {'update_time': now}})
        return token_obj
    token_obj = generate_token(token_obj)
    token_obj.update_time = datetime.now().utcnow()
    _id = mongo.tokens.insert(token_obj.__dict__)
    logging.debug("Token Created: ", token_obj.token)
    logging.debug("Token ID: ", _id)

    return token_obj


def token_is_exist(token):
    token = mongo.tokens.find_one({'token': token})
    if token:
        return True
    return False
