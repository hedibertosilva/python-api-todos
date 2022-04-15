from flask import abort
from flask import Blueprint
from flask import request

from app.libs.auth import Auth


auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/v1/login', methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    if not request.json or not email or not password:
        abort(401, description="Please, supply the credentials required.")

    return Auth.login(email=email, password=password)
