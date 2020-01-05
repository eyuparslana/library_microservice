from flask_api import status as response_status
from flask import request, Flask
from services.token.token_model import Token
from services.token import token_service

app = Flask(__name__)


@app.route('/add_token', methods=['GET'])
def add_token():
    user_id = request.args.get('user_id')
    token = Token(user_id)
    token = token_service.add_token(token)

    return {'token': token.token}, response_status.HTTP_200_OK


@app.route('/check_token/<token>', methods=['GET'])
def token_is_exist(token):
    is_exist = token_service.token_is_exist(token)
    if is_exist:
        return {}, response_status.HTTP_200_OK
    return {}, response_status.HTTP_404_NOT_FOUND


if __name__ == '__main__':
    app.run(host='localhost', port=5001)
