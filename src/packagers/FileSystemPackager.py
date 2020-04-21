import os
import urllib.request
from logging import Logger
from zipfile import ZipFile, ZIP_LZMA
from typing import List
from multiprocessing.pool import ThreadPool


from src.providers import Provider
from src.Product import Product
from .Packager import Packager

class FileSystemPackager(Packager):
    def __init__(self, logger: Logger, output_dir: str, tmp_dir: str, num_workers: int):
        super().__init__(logger, output_dir)
        self.__tmp_dir = tmp_dir
        self.__num_workers = num_workers

    def package(self, products):
        with ThreadPool(self.__num_workers) as pool:
            self._logger.info('Started Downloading')
            downloaded_paths = pool.map(self.__download, products)
            paths_to_bundle = [path for path in downloaded_paths if path]
            if len(paths_to_bundle) > 0:
                self._logger.info('Started packaging')
                package_name = self.__zip(paths_to_bundle)
                self._logger.debug(
                    'Finished packaging into file {0}'.format(package_name))
            else:
                self._logger.info('No new products - skipping packaging')

    def __get_output_file_path(self, provider: Provider, product: Product) -> str:
        package_dir = os.path.join(self.__tmp_dir, provider.name, product.name)
        os.makedirs(package_dir, exist_ok=True)
        return os.path.join(package_dir, '{0}.{1}'.format(product.version, provider.file_ext))

    def __download(self, product: Product) -> str or None:
        output_path = self.__get_output_file_path(product.provider, product)
        if not os.path.isfile(output_path):
            self._logger.debug('Started Downloading product {0}@{1} from provider {2} to file {3}'.format(product.name, product.version, product.provider.name, output_path))
            url = product.download_url
            if not url.lower().startswith('http'):
                self._logger.critical('Product download URL must start with http. received {0}'.format(url))
                raise ValueError from None
            urllib.request.urlretrieve(url, output_path)
            self._logger.info('Downloaded product {0}@{1} from provider {2}'.format(product.name, product.version, product.provider.name))

            return output_path
        else:
            self._logger.info('Skipping download for product {0}@{1} from provider {2}'.format(
                product.name, product.version, product.provider.name))

    def __zip(self, paths: List[str]) -> None:
        with ZipFile(self.output_path, 'w', compression=ZIP_LZMA) as zip_file:
            for file in paths:
                zip_file.write(file)
