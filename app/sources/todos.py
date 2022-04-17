# pylint: disable=too-few-public-methods
"""
    TODOS third-party data source.
"""
import time
from typing import Any
from typing import Dict
from typing import List
from operator import itemgetter
from flask import abort

import requests
import requests.exceptions as rexc


class Todos:
    """ Collecting third-party data source.

    Attributes:
        _data (list): Data collected. Defaults to empty list.
        _limit (int): Number of tasks that it will be returned.
        _timeout (int): Timeout requests in seconds. Defaults to 3 secods.
        _attempts (int): Number of attempts to request. Defaults to 3 attempts.
        _url (str): Defaults to "https://jsonplaceholder.typicode.com/todos".
        _sleep_time (int): Seconds to hold the execution. Defaults to 2 seconds.
    """

    _data: list = []
    _sleep_time: int = 2
    _limit: int
    _timeout: int
    _attempts: int
    _url: str

    def __init__(
        self,
        limit: int = 5,
        timeout: int = 3,
        attempts: int = 3,
        url: str = "https://jsonplaceholder.typicode.com/todos"
    ) -> None:
        """ Initializing collecting and sorting data. """
        self._limit = self._validate_int_input(limit, default=5)
        self._timeout = self._validate_int_input(timeout, default=3)
        self._attempts = self._validate_int_input(attempts, default=3)
        self._url = url

        self._get_data()
        self._sort_data()

    @staticmethod
    def _validate_int_input(value: Any, default: int) -> int:
        """ Valid input integer data.

        Args:
            value (Any): original input.
            default (int): value for unexpected errors.

        Returns:
            int: value checked.
        """
        try:
            value = int(value)
            return value if value > 0 else default
        except (TypeError, ValueError):
            return default

    def _get_data(self) -> None:
        """ Collecting data from 3rd-party source provided on URL variable

            The script will gonna try until number the attempts declarated on
            self._attempts variable.
            If the request failed for network (unreachable host) or connection
            error (DNS), it will wait until self._sleep_time to try againt.
            For all another exception (RequestException) it will raises a code
            status 400 with the message "Failed to collect data."
         """
        for attempt in range(self._attempts):
            try:
                self._data = (requests
                              .get(self._url, timeout=self._timeout)
                              .json())
            except (rexc.Timeout, rexc.ConnectionError):
                if attempt < self._attempts-1:
                    continue
            except rexc.RequestException:
                abort(400, description="Failed to collect data.")
            if not self._data:
                abort(400, description="Failed to collect data.")
            break

    def _sort_data(self) -> None:
        """ Sorting data using id key. """
        try:
            self._data = sorted(self._data, key=itemgetter("id"))
        except KeyError:
            abort(
                400,
                description="Unexpected keys in the third-party data source.")

    @property
    def data(self) -> List[Dict]:
        """ Returning the data sorted and limited. """
        return self._data[:self._limit]
