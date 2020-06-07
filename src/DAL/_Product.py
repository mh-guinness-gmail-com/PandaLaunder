class Product:
    def __init__(self, provider: str, name: str, version: str, url: str, resolved_on: str):
        """A structure that holds a single representation of a product in DAL."""
        self.__provider = provider
        self.__name = name
        self.__version = version
        self.__url = url
        self.__resolved_on = resolved_on
    
    @property
    def provider(self) -> str:
        return self.__provider
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def version(self) -> str:
        return self.__version
    
    @property
    def url(self) -> str:
        return self.__url
    
    @property
    def resolved_on(self) -> str:
        return self.__resolved_on
    