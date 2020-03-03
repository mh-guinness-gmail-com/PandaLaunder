from abc import ABC, abstractmethod
from typing import List, Tuple


class Provider(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def provide(self, products: List[str]) -> Tuple[List[Tuple[str, str, str]], str, str]:
        pass
