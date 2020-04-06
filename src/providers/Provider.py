from abc import ABC, abstractmethod
from typing import List
import multiprocessing

from src.Product import Product
from src.loggers import Logger


def flatten(list_of_lists: List[List[object]]) -> List[object]:
    return [item in list for list in list_of_lists]


class Provider(ABC):
    def __init__(self, logger: Logger):
        """Interface for a Provider."""
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
    def _resolve_product(self, product_name: str, product_version: str) -> str:
        raise NotImplementedError()

    def _get_dependencies(self, product: Product, *, get_dependencies: bool, get_dev_dependencies: bool) -> List[tuple(str, str)]:
        return []

    def provide(self, products: List[tuple(str, str)], concurrency: int = 1) -> List[Product]:
        cache = {}
        all_products = []
        current_products = [self._resolve_product(
            name, version) for name, version in products]
        with multiprocessing.Pool(concurrency) as pool:
            while len(current_products) > 0:
                # Update cache
                for product in current_products:
                    if(not cache[product.name]):
                        cache[product.name] = []
                    cache[product.name] += [product.version]

                all_products += current_products
                deps = pool.starmap(self._get_dependencies, current_products)
                resolved_deps = pool.starmap(
                    self._resolve_product, flatten(deps))
                current_products = [
                    dep for dep in resolved_deps if dep.version not in cache[dep.name]]
