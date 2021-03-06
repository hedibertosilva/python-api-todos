"""
    Provides handlers methods to control exceptions.
"""
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Response
from flask import json


def handle_error(err: HTTPException) -> Response:
    """ Handle erros raised by flask.abort method.

    Args:
        err (HTTPException): raised error.

    Returns:
        Response: HTTP response.
    """
    response = err.get_response()
    response.content_type = "application/json"
    reason = f"{err.name}. {err.description}"
    response.data = json.dumps({
        "error": {
            "reason": reason
        }
    })
    return response
