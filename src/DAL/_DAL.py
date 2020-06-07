from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from logging import Logger


from src.Product import Product
from ._Provider import Provider
from ._Product import Product as DALProduct


class DAL(ABC):
    def __init__(self, logger: Logger, params: str):
        """Interface for a DAL."""
        self._logger = logger

    def __enter__(self) -> DAL:
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.close()

    @property
    @staticmethod
    @abstractmethod
    def name() -> str:
        raise NotImplementedError()

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def add_provider(self, name: str, products: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def add_resolved_product(self, product: Product) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_providers(self) -> List[Provider]:
        raise NotImplementedError()

    @abstractmethod
    def get_products(self, provider: str = None) -> List[DALProduct]:
        raise NotImplementedError()
