class Provider:
    def __init__(self, name: str, products: str):
        """A structure that holds a single representation of a provider in DAL."""
        self.__name = name
        self.__products = products

    @property
    def name(self) -> str:
        return self.__name

    @property
    def products(self) -> str:
        return self.__products
