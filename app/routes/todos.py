from flask import Blueprint
from app.libs.auth import auth_required

todos_bp = Blueprint('todos_bp', __name__)


@todos_bp.route('/v1/todos', methods=["GET"])
@auth_required
def todos():
    return "Todos"
