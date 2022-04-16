# pylint: disable=bare-except
"""
    Provides auth tools to manage protected routes.
"""
from functools import wraps
from flask import abort
from flask import Response
from flask import request

from app.models.user import User
from app.libs.token import Token
from app.extensions.responses import success


def auth_required(func):
    """ Decorate to require authentication for the selected routes. """
    @wraps(func)
    def decorated(*args, **kwargs):
        if not Auth.is_authenticated(request.headers):
            abort(401,
                  description=(
                      "You supplied the wrong credentials! "
                      "Expecting a Bearer Token."))
        return func(*args, **kwargs)
    return decorated


class Auth:
    """ Gather all auth methods. """
    @staticmethod
    def login(**data) -> Response:
        """
            Responsible to generate a new token if the credentials was
            correctly suplied. If not, the method will raise HTTP status
            code 401 alerting about invalid login or passsword.

            Args:
                data (Any)
        """
        from flask import current_app as app


        _secret_key = app.config['SECRET_KEY']

        user = (User.query
                    .filter_by(username=data["username"])
                    .first())

        if not user:
            abort(401, description="Invalid login or password.")

        if user.is_password_correct(data["password"]):
            i_token = Token(_secret_key)
            i_token.encoding(user.id)
            return success(
                201,
                message="The token was generated successfully.",
                data={
                    "user": {
                        "id": user.id,
                        "created_at": user.created_at
                    },
                    "token": i_token.bearer_token,
                    "expires_at": i_token.expires_at
                })

        abort(401, description="Invalid login or password.")

    @staticmethod
    def is_authenticated(headers: dict) -> bool:
        """ Check if that the token supplied it's valid and
            it was associate with a valid user.

        Args:
            headers (dict): request.headers

        Returns:
            bool: Returns True if the user is authenticated. If not, False.
        """
        from flask import current_app as app


        _secret_key = app.config['SECRET_KEY']

        btoken = None
        if "Authorization" in headers:
            btoken = headers["Authorization"]

        if not Token.is_bearer(btoken):
            return False

        try:
            data = Token(_secret_key).decoding(btoken)
            user = (User.query
                        .filter_by(id=data["id"])
                        .first())
        except:
            return False
        else:
            if not user:
                return False

        return True
