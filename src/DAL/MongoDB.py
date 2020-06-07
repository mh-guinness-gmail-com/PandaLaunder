from datetime import datetime
from pymongo import MongoClient
from typing import Dict


from ._DAL import DAL
from src.Product import Product
from src.providers import get_providers


providers = { provider.name: provider for provider in get_providers() }

def _product_from_dict(product: Dict) -> Product:
    return Product(providers[product['provider']], product['name'], product['version'])

class MongoDB(DAL):
    def __init__(self, logger, params):
        super().__init__(logger, params)
        self.__client = MongoClient(params)
        self.__db = self.__client.get_default_database()

    @staticmethod
    def _get_name():
        return 'mongodb'

    def close(self):
        self.__client.close()

    def add_provider(self, provider):
        providers = self.__db['providers']
        duplicate = providers.find_one({ 'name': provider.name })
        if duplicate:
            self._logger.error("Tried to add existing provider to DB")
            raise RuntimeError()
        providers.insert_one(provider.to_dict())

    def add_resolved_product(self, product):
        resolved = self.__db['resolved']
        resolved.insert_one({
            **product.to_dict(),
            'resolved_on':  str(datetime.now()),
        })

    def get_providers(self):
        return [ providers[provider['name']] for provider in self.__db['providers'].find() ]

    def get_products(self, provider = None):
        query = None
        if provider:
            query = { 'provider': provider.name }
                
        return [ _product_from_dict(product) for product in self.__db['products'].find(query) ]
    
    def is_downloaded_before(self, product):
        compare_keys = ['provider', 'name', 'version']
        product = product.to_dict()
        query = { key: product[key] for key in compare_keys }
        duplicate = self.__db['resolved'].find_one(query)

        return bool(duplicate)

