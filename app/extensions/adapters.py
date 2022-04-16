# pylint: disable=too-few-public-methods
"""
    Provides adapters interfaces to treat third-party data.
"""
from typing import Dict
from typing import List
from flask import abort

from app.sources.todos import Todos


class TodosAdapter:
    """ Provide a simple interface to retrieve data from external sources.

    Retrieves data from third-party sources to filter to the expected
    output format and to limit the number of todos returned.

    Attributes:
        _instance (Todos): Todos instance.
        _accepted_keys (list): List of keys acceptable.
    """

    _instance: Todos
    _accepted_keys: list = ["id", "title"]

    def __init__(self, instance: Todos = None) -> None:
        self._instance = instance

    def _filter_keys(self, todos: List[Dict]) -> List[Dict]:
        """ Receives 3rd-party data to return only accepted keys.

        Args:
            todos (List[Dict]): third-party data

        Returns:
            List[Dict]: 3rd-party data if only accepted keys.
        """
        try:
            return list(
                map(lambda item: {k: item[k] for k in self._accepted_keys},
                    todos)
            )
        except KeyError:
            return abort(
                400,
                description="Unexpected keys in the third-party data source.")

    def get(self, limit: int = 5) -> List[Dict]:
        """ Returns filtered data limited by the parameter input.

        Args:
            limit (int, optional): Limits the number of TODOS returned.
                                   Defaults to 5.

        Returns:
            List[Dict]: 3rd-party filtered and limited.
        """
        todos = self._instance.all()[:limit]
        todos = self._filter_keys(todos)
        return todos
