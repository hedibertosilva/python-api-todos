from flask import json


def handle_exception(err):
    response = err.get_response()
    response.content_type = "application/json"
    response.data = json.dumps({
        "error": {
            "reason": f"{err.name}. {err.description}"
        }
    })
    return response
