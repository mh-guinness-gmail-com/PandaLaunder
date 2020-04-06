from src.loggers import Logger

class ConsoleLogger(Logger):
    def __init__(self):
        pass
    def log(self, message):
        print(message)