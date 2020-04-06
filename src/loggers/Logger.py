from abc import ABC, abstractmethod

class Logger(ABC):
    def __init__(self):
        """Interface for a Logger."""

    @abstractmethod
    def log(self, message: str) -> None:
        raise NotImplementedError()
