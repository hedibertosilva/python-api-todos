"""
    TODOS route declaration.
"""
from flask import Blueprint
from flask import jsonify
from flask import Response

from app.libs.auth import auth_required
from app.sources.todos import Todos
from app.extensions.adapters import TodosAdapter

todos_bp = Blueprint('todos_bp', __name__)


@todos_bp.route('/v1/todos', methods=["GET"])
@auth_required
def todos() -> Response:
    """ Provides a TODO list.

    This route needs authentication.
    This route allows only GET Method.

    Returns:
        Response: Returns a list of tasks from a TODO list. The response
                  follows the structure below:
                    [
                        {
                            "id": int,
                            "title": str
                        },
                        ...
                    ]
    """
    tasks = TodosAdapter(Todos())
    tasks = tasks.get(limit=5)

    return jsonify(tasks)
