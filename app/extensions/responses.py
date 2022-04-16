"""
    Provides responses methods to control success returns.
"""
from typing import Any
from flask import jsonify
from flask import Response


def success(
    code: int = 200,
    message: str = "OK.",
    data: Any = None
) -> Response:
    """ Success method formats response message.

    Args:
        code (int, optional): HTTP status codes. Defaults to 200.
        message (str, optional): Friendly message. Defaults to "OK.".
        data (Any, optional): Extra data. Defaults to None.

    Returns:
        Response: _description_
    """
    code = code if 200 <= code <= 299 else 200
    response = {
        "message": message
    }
    if data:
        response["data"] = data
    return jsonify(response), code
