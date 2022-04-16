# pylint: disable=too-few-public-methods
"""
    TODOS third-party data source.
"""
import time
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
        _timeout (int): Timeout requests in seconds. Defaults to 3 secods.
        _attempts (int): Number of attempts to request. Defaults to 3 attempts.
        _url (str): Defaults to "https://jsonplaceholder.typicode.com/todos".
        _sleep_time (int): Seconds to hold the execution. Defaults to 2 seconds.
    """

    _data: list = []
    _timeout: int = 3
    _attempts: int = 3
    _url: str = "https://jsonplaceholder.typicode.com/todos"
    _sleep_time = 2

    def __init__(self) -> None:
        """ Initializing collecting and sorting data. """
        self._get_data()
        self._sort_data()

    def _get_data(self) -> None:
        """ Collecting data from 3rd-party source provided on URL variable

            The script will gonna try until number the attempts declarated on
            self._attempts variable.
            If the request failed for network (unreachable host) or connection
            error (DNS), it will wait until self._sleep_time to try againt.
            For all another exception (RequestException) it will raises a code
            status 400 with the message "Failed to collect data."
         """
        for _ in range(self._attempts):
            try:
                self._data = (requests
                              .get(self._url, timeout=self._timeout)
                              .json())
                break
            except (rexc.Timeout, rexc.ConnectionError):
                time.sleep(self._sleep_time)
                continue
            except rexc.RequestException:
                abort(400, description="Failed to collect data.")

    def _sort_data(self) -> None:
        """ Sorting data using id key. """
        try:
            self._data = sorted(self._data, key=itemgetter("id"))
        except KeyError:
            abort(
                400,
                description="Unexpected keys in the third-party data source.")

    def all(self) -> List[Dict]:
        """ Returning the data sorted. """
        return self._data
