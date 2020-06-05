from abc import ABC, abstractmethod


class Email(ABC):
    def __init__(self, smtp_server, smtp_server_port, secure):
        self.smtp_server = smtp_server
        self.smtp_server_port = smtp_server_port

    @abstractmethod
    def send_email(self, from, to, cc, bcc):
        pass
