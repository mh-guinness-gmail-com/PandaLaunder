from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from logging import Logger

from src.Product import Product
from ._Provider import Provider

class DAL(ABC):
    def __init__(self, logger: Logger, params: str):
        """Interface for a DAL."""
        self._logger = logger

    def __enter__(self) -> DAL:
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.close()

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def add_provider(self, name: str, packages: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def add_resolved_product(self, product: Product) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_providers(self) -> List[Provider]:
        raise NotImplementedError()

    @abstractmethod
    def get_products(self, provider: str = None) -> List[str]:
        raise NotImplementedError()
