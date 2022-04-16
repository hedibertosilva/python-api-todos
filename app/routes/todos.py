"""
    TODOS route declaration.
"""
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import Response

from app.libs.auth import auth_required
from app.sources.todos import Todos
from app.extensions.serializers import TodosSerializer

todos_bp = Blueprint('todos_bp', __name__)


@todos_bp.route('/v1/todos', methods=["GET"])
@auth_required
def todos() -> Response:
    """ Provides a TODO list.

    This route needs authentication.
    This route allows only GET Method.

    Request Args:
        - limit: number of tasks that it will be returned.

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
    try:
        number_of_tasks = int(request.args.get('limit', default=5))
    except ValueError:
        number_of_tasks = 5

    tasks = TodosSerializer(Todos(limit=number_of_tasks))

    return jsonify(tasks.data)
