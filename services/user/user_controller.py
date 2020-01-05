from bcrypt import hashpw
from flask import request, Flask
from flask_api import status as response_status
from flask_expects_json import expects_json
import utils
from services.user import user_service
from services.user.user_model import UserModel

app = Flask(__name__)

schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
    },
    'required': ['username', 'password']
}


@app.route("/user", methods=['POST'])
@expects_json(schema)
def register():
    request_data = request.get_json(force=True)
    username = request_data['username']
    password = hashpw(request_data['password'].encode(), utils.PASS_SALT)

    user = UserModel(username, password)

    message, is_registered = user_service.register(user)
    status = response_status.HTTP_201_CREATED
    if not is_registered:
        status = response_status.HTTP_400_BAD_REQUEST

    return message, status


@app.route("/user", methods=['PUT'])
@expects_json(schema)
def update():
    request_data = request.get_json(force=True)
    username = request_data['username']
    password = hashpw(request_data['password'].encode(), utils.PASS_SALT)
    user_id = request_data["id"]

    user = UserModel(username, password)
    message, is_updated = user_service.update(user, user_id)
    status = response_status.HTTP_200_OK
    if not is_updated:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


@app.route("/user/<user_id>", methods=['DELETE'])
def delete(user_id):
    message, is_created = user_service.delete(user_id)
    status = response_status.HTTP_200_OK
    if not is_created:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


@app.route("/user/<user_id>", methods=['GET'])
def get(user_id):
    message, is_created = user_service.get_user_by_id(user_id)
    status = response_status.HTTP_200_OK
    if not is_created:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


@app.route("/users", methods=['GET'])
def get_all_user():
    message, is_created = user_service.get_all_users()
    status = response_status.HTTP_200_OK
    if not is_created:
        status = response_status.HTTP_404_NOT_FOUND
    print(message)
    return message, status


@app.route("/login", methods=['POST'])
@expects_json(schema)
def login():
    request_data = request.get_json(force=True)
    username = request_data['username']
    password = hashpw(request_data['password'].encode(), utils.PASS_SALT)

    user = UserModel(username, password)
    message, is_created = user_service.login(user)
    status = response_status.HTTP_200_OK
    if not is_created:
        status = response_status.HTTP_404_NOT_FOUND
    return message, status


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
