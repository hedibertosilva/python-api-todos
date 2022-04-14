from flask import Blueprint
from flask import request

from app.libs.auth import Auth


auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route('/v1/login', methods=["POST"])
def login():
    return Auth.login(request)


@auth_blueprint.route('/v1/signup', methods=["POST"])
def signup():
    return Auth.signup(request)