import os
import io
import requests
from logging import Logger
from zipfile import ZipFile, ZIP_LZMA
from typing import List


from src.providers import Provider
from src.Product import Product
from .Packager import Packager


class InMemoryPackager(Packager):
    def package(self, products):
        with io.BytesIO() as mem_file:
            zip_file = ZipFile(mem_file, mode='w', compression=ZIP_LZMA)
            self._logger.info('Started Downloading')
            for product in products:
                product_descriptor = 'product {0}@{1} from provider {2}'.format(product.name, product.version, product.provider.name)
                self._logger.debug('Downloading {0}'.format(product_descriptor))
                path = '{0}/{1}/{2}.{3}'.format(product.provider.name, product.name, product.version, product.provider.file_ext)
                file = requests.get(product.download_url)
                self._logger.debug('Done downloading {0}'.format(product_descriptor))
                self._logger.debug('Packaging {0}'.format(product_descriptor))
                zip_file.writestr(path, file.content)
                self._logger.info('Added {0}'.format(product_descriptor))
            self._logger.debug('Done downloading')
            zip_file.close()

            self._logger.debug('Saving to file')
            with open(self.output_path, 'wb') as file:
                file.write(mem_file.getbuffer())
