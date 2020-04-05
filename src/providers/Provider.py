from abc import ABC, abstractmethod
from typing import List, Tuple


class Provider(ABC):
    def __init__(self):
        """
<<<<<<< HEAD
        Interface for a Provider.
        A Provider is a class which is responsible for resolving download links,
=======
        Interface for a Provider. 
        A Provider is a class which is responsible for resolving download links
>>>>>>> fb2cc0031ad2224836bd957c20938422420e13e9
        for its respective product, for example an npm-package(product) and npm (Provider)
        pip-package(product) and pip (provider).
        """
        pass

    @abstractmethod
    def provide(self, products: List[str]) -> Tuple[List[Tuple[str, str, str]], str, str]:
        pass
