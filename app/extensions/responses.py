from typing import Any
from flask import jsonify
from flask import Response


def success(code: int = 200, message: str = "OK.", data: Any = None) -> Response:
    code = code if 200 <= code <= 299 else 200
    obj = {
        "message": message
    }
    if data:
        obj["data"] = data
    return jsonify(obj), code
