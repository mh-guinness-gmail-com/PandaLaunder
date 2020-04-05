from abc import ABC, abstractmethod
from typing import List, Tuple


class Provider(ABC):
    def __init__(self):
        """
        Interface for a Provider. 
        A Provider is a class which is responsible for resolving download links
        for its respective product, for example an npm-package(product) and npm (Provider)
        pip-package(product) and pip (provider).
        """
        pass

    @abstractmethod
    def provide(self, products: List[str]) -> Tuple[List[Tuple[str, str, str]], str, str]:
        pass
