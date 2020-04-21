from abc import ABC, abstractmethod
from typing import List
from logging import Logger
import uuid
import os


from src.Product import Product


class Packager(ABC):
    def __init__(self, logger: Logger, output_dir: str):
        """Interface for a Packager."""
        self._logger = logger
        os.makedirs(output_dir, exist_ok=True)
        self.__output_path = '{0}/{1}.zip'.format(output_dir, uuid.uuid4())
    
    @property
    def output_path(self) -> str:
        return self.__output_path

    @abstractmethod
    def package(self, products: List[Product]) -> None:
        raise NotImplementedError()
