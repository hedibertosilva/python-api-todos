"""
    Authentication route declaration.
"""
from flask import abort
from flask import Blueprint
from flask import Response
from flask import request

from app.libs.auth import Auth


auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/v1/login', methods=["POST"])
def login() -> Response:
    """ Provides authentications for users registered.

    This route needs authentication.
    This route allows only POST Method and needs a body application/json
    following the body structure below:
        {
            "username": str,
            "password": str
        }

    Returns:
        Response: Provides utils informations about bearer token and user. The
                  response follow the structure below:
                    {
                        "data": {
                            "expires_at": str,
                            "token": str,
                            "user": {
                                "created_at": str,
                                "id": int
                            }
                        },
                        "message": str
                    }
                  If username or password data wasn't supplied on body, returns
                  status code 400 on follow structure:
                    {
                        "error": {
                            "reason": "Unauthorized. Please, supply the
                                       credentials required."
                        }
                    }
    """
    username = request.json.get("username")
    password = request.json.get("password")

    if not request.json or not username or not password:
        abort(400, description="Please, supply the credentials required.")

    return Auth.login(username=username, password=password)
