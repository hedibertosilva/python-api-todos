import os
import jwt
from datetime import datetime
from datetime import timedelta
from flask import request
from functools import wraps
from werkzeug.security import check_password_hash

from app.models.user import User


_SECRET_KEY = os.environ['SECRET_KEY']


def auth_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not Auth.is_authenticated(request):
            return {
                    "error": {
                        "reason": "Authorization required."
                    }
                }, 401
        return func(*args, **kwargs)
    return decorated


class Auth:
    @staticmethod
    def login(request):
        auth = request.json
        if not auth or not auth.get('email') or not auth.get('password'):
            return {
                    "error": {
                        "reason": "Missing login data. Please, check if there"\
                                   + " are any missing information."
                    }
                }, 401

        user = (User.query
                        .filter_by(email = auth.get('email'))\
                        .first())

        if not user:
            return {
                    "error": {
                        "reason": "User does not exist. Please, check that" \
                            + " all the information you provided is correct."
                    }
                }, 401
        if user.is_password_correct(auth.get('password')):
            expires_at = str(datetime.utcnow() + timedelta(minutes = 30))
            token = jwt.encode({
                'id': user.id,
                'expires_at': expires_at
            }, _SECRET_KEY)
            return {
                    "token": token.decode('UTF-8'),
                    "expires_at": expires_at
                }, 201
        return {
                "error": {
                    "reason": "The password you entered is incorrect."
                }
            }, 403

    @staticmethod
    def signup(request):
        data = request.json

        email = data.get("email")
        password = data.get("password")

        # checking for existing user
        user = (User.query
                    .filter_by(email = email)\
                    .first())
        if not user:
            # database ORM object
            user = User(
                email = email,
                password = password
            )
            user.save()

            return {
                "success": {
                    "message": "The user was successfully registered."
                }
            }, 201
        else:
            return {
                "success": {
                    "message": "User already exists. Please Log in."
                }
            }, 202

    @staticmethod
    def is_authenticated(request) -> bool:
        token = None

        if 'Authorization' in request.headers:
            btoken = request.headers['Authorization']
            token = btoken.split('Bearer ')[-1]

        if not token:
            return False

        try:
            data = jwt.decode(token, _SECRET_KEY)
            User.query \
                    .filter_by(id = data['id'])\
                    .first()
        except Exception as err:
            return False

        return True