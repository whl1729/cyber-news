from abc import ABC
from abc import abstractmethod
from typing import List


class WebParser(ABC):
    @abstractmethod
    def parse(self, resp_text: str) -> List[dict]:
        return []
