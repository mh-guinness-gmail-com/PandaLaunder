from src.loggers.Logger import Logger

class ConsoleLogger(Logger):
    def log(self, message):
        print(message)