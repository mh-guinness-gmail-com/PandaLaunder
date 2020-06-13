from __future__ import annotations
from abc import ABC, abstractmethod, ABCMeta
from typing import List
from logging import Logger


from src.Product import Product
from src.providers import Provider

class MetaDAL(ABCMeta):
    @property
    def name(self) -> str:
        return self._get_name()

class DAL(ABC, metaclass=MetaDAL):
    def __init__(self, logger: Logger, params: str):
        """Interface for a DAL."""
        self._logger = logger

    def __enter__(self) -> DAL:
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.close()

    @staticmethod
    @abstractmethod
    def _get_name() -> str:
        raise NotImplementedError()

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def add_provider(self, provider: Provider) -> None:
        raise NotImplementedError()

    @abstractmethod
    def add_resolved_products(self, products: List[Product]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_providers(self) -> List[Provider]:
        raise NotImplementedError()

    @abstractmethod
    def get_products(self, provider: Provider = None) -> List[Product]:
        raise NotImplementedError()

    @abstractmethod
    def is_downloaded_before(self, product: Product) -> bool:
        raise NotImplementedError()
