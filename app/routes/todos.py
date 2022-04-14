from flask import Blueprint
from app.libs.auth import auth_required

todos_blueprint = Blueprint('todos_blueprint', __name__)


@todos_blueprint.route('/v1/todos', methods=["GET"])
@auth_required
def todos():
    return "Todos"
