from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from logging import Logger

from .Provider import Provider

class DAL(ABC):
    def __init__(self, logger: Logger):
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
    def get_providers(self) -> List[Provider]:
        raise NotImplementedError()

    @abstractmethod
    def get_products(self, provider: str) -> List[str]:
        raise NotImplementedError()
