"""
    SERIALIZERS: unit tests.
"""
from werkzeug.exceptions import BadRequest

from app.extensions.serializers import TodosSerializer
from app.helpers.json import JSON


def test_serializer(todos_mock):
    """ Testing TodosSerializer class. """
    serialized = TodosSerializer(todos_mock())

    assert serialized.data == JSON.read_file("tests/data/todos_serialized.json")


def test_serializer_missing_required_keys(todos_missing_required_keys_mock):
    """ Testing TodosSerializer class with data missing keys. """
    try:
        TodosSerializer(todos_missing_required_keys_mock()).data
        assert 0
    except BadRequest as err:
        assert err.code == 400
        assert err.name == "Bad Request"
        assert err.description == "Unexpected keys in the third-party data source."


def test_serializer_with_unexpected_format(todos_unexpected_format_mock):
    """ Testing TodosSerializer class with an unexpected format. """
    try:
        TodosSerializer(todos_unexpected_format_mock()).data
        assert 0
    except BadRequest as err:
        assert err.code == 400
        assert err.name == "Bad Request"
        assert err.description == "Unexpected keys in the third-party data source."


def test_serializer_add_new_required_key(todos_mock):
    """ Testing TodosSerializer class add a new required key. """
    serialized = TodosSerializer(todos_mock(), accepted_keys=["id", "title", "completed"])

    assert serialized.data == JSON.read_file("tests/data/todos_with_new_required_key.json")
