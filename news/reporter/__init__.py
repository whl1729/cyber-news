from abc import ABC
from abc import abstractmethod


class Reporter(ABC):
    @abstractmethod
    def report(self) -> str:
        raise Exception("Not Implemented")
