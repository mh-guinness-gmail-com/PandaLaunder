from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
from threading import Lock, Thread
from logging import Logger
from queue import Queue

from src.Product import Product


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
        cache_lock = Lock()
        all_products = []
        product_queue = Queue()

        threads = [Thread(target=self.__provide_worker, args=[
                          product_queue, all_products, cache, cache_lock], daemon=True)for _ in range(concurrency)]
        for t in threads:
            t.start()

        for product in products:
            product_queue.put(product)

        # Wait for threads to finish and kill them
        product_queue.join()
        for _ in threads:
            product_queue.put(None)
        for thread in threads:
            thread.join()

        return all_products

    def __provide_worker(self, product_queue: Queue, result_set: List[Product], cache: Dict[str, List[str]], cache_lock: Lock):
        for name, version in iter(product_queue.get, None):
            try:
                resolved = self._resolve_product(name, version)
                with cache_lock:
                    if resolved.name not in cache:
                        cache[resolved.name] = []
                    if resolved.version in cache[resolved.name]:
                        continue
                    cache[resolved.name].append(resolved.version)
                result_set.append(resolved)
                dependencies = self._get_dependencies(resolved)
                for dependency in dependencies:
                    product_queue.put(dependency)
            finally:
                product_queue.task_done()
