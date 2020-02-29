from ABC import ABC, abstractmethod
from typing import List, Tuple


class Provider(ABC):
    __init__(self):
        pass

    @abstractmethod
    def provide(products: List[str]) -> Tuple[List[str], str, str]:
        pass
