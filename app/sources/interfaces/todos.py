from abc import ABC, abstractmethod
from typing import Dict
from typing import List


class AbstractTodos(ABC):

    def __init__(
        self,
        limit: int,
        timeout: int,
        attempts: int,
        url: str
    ) -> None:
        """ Input parameters required. """
        ...

    @property
    @abstractmethod
    def data(self) -> List[Dict]:
        """ Returning the data sorted and limited. """
        ...
