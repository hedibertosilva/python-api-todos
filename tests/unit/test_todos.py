"""
    TODOS: unit tests.
"""
import pytest
from werkzeug.exceptions import BadRequest

from app.sources.todos import Todos


def test_source_todos():
    """ Testing if normal response returns with expected keys
        and limited by default.
    """
    todos = Todos().data

    required_keys = ["id", "title"]

    assert isinstance(todos, list)
    assert len(todos) == 5
    assert set(required_keys) <= todos[0].keys()

def test_source_todos_with_invalid_url():
    """ Testing request with a wrong URL. """

    try:
        Todos(
            url="https://jsonplaceholder.typicode.com/"
        ).data
        assert 0
    except BadRequest as err:
        assert err.code == 400
        assert err.name == "Bad Request"
        assert err.description == "Failed to collect data."

def test_source_todos_with_unreachable_host():
    """ Testing request with a unreachable host. """

    try:
        Todos(
            url="https://10.10.10.10/"
        ).data
        assert 0
    except BadRequest as err:
        assert err.code == 400
        assert err.name == "Bad Request"
        assert err.description == "Failed to collect data."

@pytest.mark.parametrize("limit", [1, 2])
def test_source_todos_with_valid_limit(todos, limit):
    """ Testing if the response returns limited. """
    assert len(todos) == limit


@pytest.mark.parametrize("limit", ['a', 'b'])
def test_source_todos_with_invalid_limit(todos):
    """ Testing if the response returns 5 elements by default to
        unexpected limit input. """
    assert len(todos) == 5
