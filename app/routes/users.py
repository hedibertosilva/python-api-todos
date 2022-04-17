"""
    Users route declaration.
"""
from flask import abort
from flask import Blueprint
from flask import request
from flask import Response

from app import logging
from app.models.user import User
from app.extensions.responses import success


users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/v1/users', methods=["POST"])
def users() -> Response:
    """ Provides the register to new users.

    This route allows only POST Method and needs a body application/json
    following the body structure below:
        {
            "username": str,
            "password": str
        }

    Returns:
        Response: If the user supplied it was created, returns status code 201.
                  The response follows the folling the following structure:
                    {
                        "data": {
                            "created_at": str,
                            "username": str,
                            "id": int
                        },
                        "message": "The user has been successfully registered."
                    }
                  If user already exists, returns status code 202 on structure:
                    {
                        "message": "User already exists."
                    }
                  If username or password data wasn't supplied on body, returns
                  status code 400:
                    {
                        "error": {
                            "reason": "Bad Request. Please, supply the username
                                       and password data."
                        }
                    }
    """
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        abort(400,
              description="Please, supply the username and password data.")

    user = (User.query
                .filter_by(username=username)
                .first())

    if not user:
        logging.debug(
            f"[USER] [REGISTRATION] New user added. Username {username}")
        i_user = User(username=username, password=password)
        i_user.save()
        return success(
            201,
            message="The user has been successfully registered.",
            data={
                "id": i_user.id,
                "username": i_user.username,
                "created_at": i_user.created_at
            })

    return success(202, message="User already exists.")
