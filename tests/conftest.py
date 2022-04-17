import os
import pytest
from typing import Dict
from typing import List
from app import create_app
from app.helpers.json import JSON
from app.sources.todos import Todos


# CLASS TO UNIT TESTS.


class TodosMock:
    @property
    def data(self) -> List[Dict]:
        return JSON.read_file("tests/data/todos_original.json")


class TodosMissingRequiredKeysMock:
    @property
    def data(self) -> List[Dict]:
        return JSON.read_file("tests/data/todos_missing_required_keys.json")


class TodosUnexpectedFormatMock:
    @property
    def data(self) -> List[Dict]:
        return JSON.read_file("tests/data/todos_unexpected_format.json")


# FIXTURES TO UNIT TESTS.


@pytest.fixture
def todos(limit):
    """ Collecting data from external api. """
    return Todos(limit=limit).data


@pytest.fixture
def todos_mock():
    """ Loading TodosMock class. """
    return TodosMock


@pytest.fixture
def todos_missing_required_keys_mock():
    """ Loading TodosMissingRequiredKeysMock class. """
    return TodosMissingRequiredKeysMock


@pytest.fixture
def todos_unexpected_format_mock():
    """ Loading TodosUnexpectedFormatMock class. """
    return TodosUnexpectedFormatMock


# FIXTURES TO FUNCTIONAL TESTS.


@pytest.fixture
def test_client():
    """ Testing app. """
    app = create_app("testing.cfg")
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture
def btoken(test_client):
    """ Logging on the app. """
    default_admin_user = os.environ.get("ADMIN_USER", "admin")
    default_admin_password = os.environ.get("ADMIN_PASSWORD", "admin")

    response = test_client.post("/v1/login",
                                json={
                                    "username": default_admin_user,
                                    "password": default_admin_password
                                })

    return response.json["data"]["token"]
