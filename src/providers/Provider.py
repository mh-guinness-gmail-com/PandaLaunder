from abc import ABC, abstractmethod
from typing import List, Tuple
import multiprocessing

from src.Product import Product
from src.loggers import Logger


def flatten(list_of_lists: List[List[object]]) -> List[object]:
    return [item for item_list in list_of_lists for item in item_list]


class Provider(ABC):
    def __init__(self, logger: Logger):
        """Interface for a Provider."""
        self._logger = logger

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

    def _get_dependencies(self, product: Product, *, get_dependencies: bool = True, get_dev_dependencies: bool = False) -> List[Tuple[str, str]]:
        return []

    def provide(self, products: List[Tuple[str, str]], concurrency: int = 1) -> List[Product]:
        cache = {}
        all_products = []
        current_products = [self._resolve_product(
            name, version) for name, version in products]
        with multiprocessing.Pool(concurrency) as pool:
            while len(current_products) > 0:
                # Update cache
                for product in current_products:
                    if(product.name not in cache):
                        cache[product.name] = []
                    cache[product.name] += [product.version]

                all_products += current_products
                deps = set(flatten(pool.map(self._get_dependencies, current_products)))
                resolved_deps = pool.starmap(self._resolve_product, deps)
                current_products = [
                    dep for dep in resolved_deps if dep.name not in cache or dep.version not in cache[dep.name]]
        return all_products
