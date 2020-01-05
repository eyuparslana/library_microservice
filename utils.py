from datetime import datetime

import bson
from flask_pymongo import PyMongo
import json


PASS_SALT = b'$2b$12$p3xjIA41VrzJaSzkEmuoO.'
TIME_FORMAT = "%d/%m/%Y %H:%M:%S"

SECRET_KEY = "2F939CAB6EF2A8E334695FE3A76C8"
JWT_ALGORITHM = "HS256"

TOKEN_SERVICE_URL = "http://localhost:5001"
AUTHOR_SERVICE_URL = "http://localhost:5002"
BOOK_SERVICE_URL = "http://localhost:5003"
BOOK_STOCK_SERVICE_URL = "http://localhost:5005"


def serialize(x):
    if isinstance(x, datetime):
        return x.strftime('%d/%m/%Y')
    elif isinstance(x, bson.objectid.ObjectId):
        return str(x)
    elif isinstance(x, bytes):
        return x.decode()
    else:
        raise TypeError(x)


def config(app):
    app.config["MONGO_URI"] = "mongodb://localhost:27017/library"
    mongo = PyMongo(app)

    return app, mongo.db


def result_serializer(bson_data):
    print(bson_data)
    if not isinstance(bson_data, list):
        return json.loads(json.dumps(bson_data, default=serialize))

    result = []
    for user in list(bson_data):
        result.append(json.loads(json.dumps(user, default=serialize)))
    return result
