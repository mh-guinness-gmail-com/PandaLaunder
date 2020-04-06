from abc import ABC, abstractmethod

from src.Product import Product
from src.Logger import Logger


class DAL(ABC):
    def __init__(self, logger: Logger):
        """Interface for a DAL."""
        self.__logger = logger

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def file_ext(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def resolve_product(self, product_name: str, product_version: str) -> str:
        raise NotImplementedError()

    def get_dependencies(self, product: Product, *, get_dependencies: bool, get_dev_dependencies: bool) -> List[tuple(str, str)]:
        return []
