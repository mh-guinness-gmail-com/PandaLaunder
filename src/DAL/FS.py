import yaml
from datetime import datetime


from ._DAL import DAL
from src.Product import Product
from src.providers import get_providers


providers = { provider.name: provider for provider in get_providers() }

class FS(DAL):
    def __init__(self, logger, params):
        super().__init__(logger, params)
        self.__path = params
        self.__load()
        self.__init_empty_db()
        self.__flush()

    def __init_empty_db(self) -> None:
        if not self.__content:
            self.__content = {}
        content = self.__content
        if 'providers' not in content:
            content['providers'] = []
        if 'products' not in content:
            content['products'] = []
        if 'resolved' not in content:
            content['resolved'] = []

    def __load(self) -> None:
        with open(self.__path, 'r+') as file:
            self.__content = yaml.load(file.read())

    def __flush(self) -> None:
        with open(self.__path, 'w') as file:
            file.write(yaml.dump(self.__content))

    @staticmethod
    def _get_name():
        return 'fs'

    def close(self):
        self.__flush()

    def add_provider(self, provider):
        c_providers = self.__content['providers']
        duplicates = [ p for p in c_providers if p['name'] == provider.name ]
        if len(duplicates) > 0:
            self._logger.error("Tried to add existing provider to DB")
            raise RuntimeError()
        c_providers.append(provider.to_dict())
        self.__flush()

    def add_resolved_product(self, product):
        resolved = self.__content['resolved']
        resolved.append({ 
            **product.to_dict(),
            'resolved_on':  str(datetime.now()),
        })
        self.__flush()

    def get_providers(self):
        return [ providers[provider['name']] for provider in self.__content['providers'] ]

    def get_products(self, provider = None):
        return [
            Product(**product)
            for product in self.__content['products']
            if product['provider'] == provider or not provider
        ]
