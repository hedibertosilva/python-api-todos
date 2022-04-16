from flask import Blueprint
from flask import jsonify

from app.libs.auth import auth_required
from app.sources.todos import Todos
from app.extensions.adapters import TodosAdapter

todos_bp = Blueprint('todos_bp', __name__)


@todos_bp.route('/v1/todos', methods=["GET"])
@auth_required
def list():
    todos = TodosAdapter(Todos())
    todos = todos.get(limit=5)

    return jsonify(todos)
