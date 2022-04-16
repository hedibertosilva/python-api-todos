from typing import Dict
from typing import List
from app.helpers.json import JSON
from app.sources.todos import Todos

import pytest


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
