import os
import urllib.request

from src.loggers import Logger
from src.providers import Provider
from src.Product import Product


class Downloader:
    def __init__(self, base_dir: str, overwrite: bool = False, *, logger: Logger):
        self.__base_dir = base_dir
        self.__overwrite = overwrite
        self.__logger = logger

    def __get_output_file_path(self, provider: Provider, product: Product) -> str:
        package_dir = os.path.join(
            self.__base_dir, provider.name, product.name)
        os.makedirs(package_dir, mode=666, exist_ok=True)
        return os.path.join(package_dir, product.version + '.' + provider.file_ext)

    def download(self, provider: Provider, product: Product) -> str or None:
        output_path = self.__get_output_file_path(provider, product)
        if self.__overwrite or not os.path.isfile(output_path):
            urllib.request.urlretrieve(product.download_url, output_path)
            return output_path
