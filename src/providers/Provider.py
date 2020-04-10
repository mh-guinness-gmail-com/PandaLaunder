from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
from threading import Lock
from logging import Logger

from src.Product import Product
from src.ThreadPool import ThreadPool

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

    # pylint: disable=no-self-use
    def _get_dependencies(self, product: Product, *, get_dependencies: bool = True, get_dev_dependencies: bool = False) -> List[Tuple[str, str]]:
        return []

    def provide(self, products: List[Tuple[str, str]], concurrency: int = 1) -> List[Product]:
        cache = {}
        cache_lock = Lock()
        all_products = []
        args=[all_products, cache, cache_lock]
        with ThreadPool(self.__provide_worker, thread_count=concurrency, action_parameters=args) as pool:
            pool.add_tasks(products)
        return all_products

    def __provide_worker(self, product: Tuple[str, str], result_set: List[Product], cache: Dict[str, List[str]], cache_lock: Lock) -> List[Tuple[str, str]]:
        name, version = product
        resolved = self._resolve_product(name, version)
        with cache_lock:
            if resolved.name not in cache:
                cache[resolved.name] = []
            if resolved.version in cache[resolved.name]:
                return []
            cache[resolved.name].append(resolved.version)
        result_set.append(resolved)
        dependencies = self._get_dependencies(resolved)
        return dependencies
