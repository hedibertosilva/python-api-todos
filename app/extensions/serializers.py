# pylint: disable=too-few-public-methods
"""
    Provides a serializer interface to treat third-party data.
"""
from typing import Dict
from typing import List
from flask import abort

from app.sources.todos import Todos


class TodosSerializer:
    """ Provide a simple interface to serialize data from external sources.

    Retrieves data from third-party sources to filter to the expected
    output format.

    Attributes:
        _instance (Todos): Todos instance.
        _accepted_keys (list): List of keys acceptable.
    """

    _instance: Todos
    _accepted_keys: list

    def __init__(
        self,
        instance: Todos = None,
        accepted_keys: List[str] = ["id", "title"]
    ) -> None:
        self._instance = instance
        self._accepted_keys = accepted_keys

    def _filter_keys(self, todos: List[Dict]) -> List[Dict]:
        """ Receives 3rd-party data to return only accepted keys.

        Args:
            todos (List[Dict]): third-party data.

        Returns:
            List[Dict]: 3rd-party data if only accepted keys.
        """
        try:
            return list(
                map(lambda item: {k: item[k] for k in self._accepted_keys},
                    todos)
            )
        except (TypeError, KeyError):
            return abort(
                400,
                description="Unexpected keys in the third-party data source.")

    @property
    def data(self) -> List[Dict]:
        """ Returns filtered data limited by the parameter input.

        Returns:
            List[Dict]: 3rd-party filtered and limited.
        """
        response = self._filter_keys(self._instance.data)
        return response
