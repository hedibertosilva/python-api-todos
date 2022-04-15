from flask import abort
from flask import request
from flask.wrappers import Request
from functools import wraps

from app.models.user import User
from app.libs.token import Token
from app.extensions.responses import success


def auth_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not Auth.is_authenticated(request):
            abort(401, description="You supplied the wrong credentials! Expecting a Bearer Token.")
        return func(*args, **kwargs)
    return decorated


class Auth:

    @staticmethod
    def login(**data) -> None:
        user = (User.query
                    .filter_by(email=data["email"])
                    .first())

        if not user:
            abort(401, description="Invalid login or password.")

        if user.is_password_correct(data["password"]):
            i_token = Token()
            i_token.encoding(user.id)
            return success(
                201,
                message="The token was generated successfully.",
                data={
                    "user": {
                        "id": user.get_id(),
                        "created_at": user.created_at
                    },
                    "token": f"{i_token.type} {i_token.token}",
                    "expires_at": i_token.expires_at
                })

        abort(401, description="Invalid login or password.")

    @staticmethod
    def is_authenticated(request: Request) -> bool:
        btoken = None
        if "Authorization" in request.headers:
            btoken = request.headers["Authorization"]

        if not btoken:
            return False

        try:
            data = Token.decoding(btoken)
            user = (User.query
                        .filter_by(id=data["id"])
                        .first())
        except:
            return False
        else:
            if not user:
                return False

        return True
