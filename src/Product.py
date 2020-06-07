from typing import Type


from .providers import Provider


class Product:
    def __init__(self, provider: Type[Provider], name: str, version: str, download_url: str):
        """A structure that holds a single product."""
        self.__provider = provider
        self.__name = name
        self.__version = version
        self.__download_url = download_url

    @property
    def provider(self) -> Type[Provider]:
        return self.__provider

    @property
    def name(self) -> str:
        return self.__name

    @property
    def version(self) -> str:
        return self.__version

    @property
    def download_url(self) -> str:
        return self.__download_url
