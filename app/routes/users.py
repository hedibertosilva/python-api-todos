from flask import abort
from flask import Blueprint
from flask import request

from app.models.user import User
from app.libs.auth import auth_required
from app.extensions.responses import success


users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/v1/users', methods=["POST"])
@auth_required
def users():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        abort(400, description="Please, supply the email and password data.")

    user = (User.query
                .filter_by(email=email)
                .first())

    if not user:
        i_user = User(email=email, password=password)
        i_user.save()
        return success(
            201,
            message="The user has been successfully registered.",
            data={
                "id": i_user.id,
                "email": i_user.email,
                "created_at": i_user.created_at
            })

    return success(202, message="User already exists.")
