import time
import requests
import requests.exceptions as rexc
from flask import abort
from typing import Dict
from typing import List
from operator import itemgetter


class Todos:

    _data: list = []
    _timeout: int = 3
    _attempts: int = 3
    _url: str = "https://jsonplaceholder.typicode.com/todos"

    def __init__(self) -> None:
        self._get_data()
        self._sort_data()

    def _get_data(self) -> None:
        for _ in range(self._attempts):
            try:
                self._data = (requests
                                .get(self._url, timeout=self._timeout)
                                .json())
                break
            except (rexc.Timeout, rexc.ConnectionError):
                # If requests failed , it waits 2 sec and try again.
                time.sleep(2)
                continue
            except rexc.RequestException:
                # All exceptions explicitly raises RequestException
                abort(400, description="Failed to collect TODOS data.")

    def _sort_data(self) -> None:
        self._data = sorted(self._data, key=itemgetter("id"))

    def all(self) -> List[Dict]:
        return self._data
