"""The providers module exports all providers.
It also includes metadata for each provider to assist usage
"""
from typing import List

from src.DAL import DAL
from src.DAL.Provider import Provider as DALProvider
from src.providers.Provider import Provider as ProviderClass

class __Provider(DALProvider):
    def __init__(self, provider: DALProvider):
        super().__init__(provider.name, provider.products)

        class_name = '{0}'.format(str(provider.name).capitalize())
        self.__class = __import__(class_name, globals(), locals(), [],  1).__dict__[class_name]
    
    @property
    def provider_class(self) -> ProviderClass:
        return self.__class

def get_providers(db: DAL) -> List[__Provider]:
    return [ __Provider(provider) for provider in db.get_providers() ]
