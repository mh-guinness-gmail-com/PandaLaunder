import os
import urllib.request
from logging import Logger


from src.providers import Provider
from src.Product import Product


class Downloader:
    def __init__(self, base_dir: str, overwrite: bool = False, *, logger: Logger):
        """Downloads a single products at a time to a given location."""
        self.__base_dir = base_dir
        self.__overwrite = overwrite
        self.__logger = logger

    def __get_output_file_path(self, provider: Provider, product: Product) -> str:
        package_dir = os.path.join(
            self.__base_dir, provider.name, product.name)
        os.makedirs(package_dir, exist_ok=True)
        return os.path.join(package_dir, '{0}.{1}'.format(product.version, provider.file_ext))

    def download(self, product: Product) -> str or None:
        output_path = self.__get_output_file_path(product.provider, product)
        if self.__overwrite or not os.path.isfile(output_path):
            self.__logger.debug('Started Downloading product {0}@{1} from provider {2} to file {3}'.format(
                product.name, product.version, product.provider.name, output_path))
            if not product.download_url.lower().startswith('http'):
                self.__logger.critical(
                    'Product download URL must start with http. received {0}'.format(product.download_url))
                raise ValueError from None
            urllib.request.urlretrieve(product.download_url, output_path)
            self.__logger.info('Downloaded product {0}@{1} from provider {2}'.format(
                product.name, product.version, product.provider.name))

            return output_path
        else:
            self.__logger.info('Skipping download for product {0}@{1} from provider {2}'.format(
                product.name, product.version, product.provider.name))
