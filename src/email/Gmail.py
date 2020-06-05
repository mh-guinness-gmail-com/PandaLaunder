from .email.Email import Email
from email.message import EmailMessage
import smtplib, ssl
from typing import List


class Gmail(Email):
    def __init__(self, smtp_server, smtp_server_port, username, password):
        super().__init__(self, smtp_server, smtp_server_port)
        self.username = username
        self.password = password

    def send_mail(self, to: List[str] or str, message: EmailMessage):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_server_port, context=context) as server:
            # logins everytime, if we send email too frequently we can run a queue
            server.login(self.username, self.password)
            server.send_message(message, self.username, to)
