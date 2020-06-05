from email.message import EmailMessage
from typing import List, Dict
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def generate_email_message(fromMail: str, to: List[str] or str, cc: List[str] or str, bcc: List[str] or str, subject: str, template_string: str, values_dict: Dict[str, str]):
    message = MIMEMultipart()
    message["From"] = fromMail
    message["To"] = to
    message["Subject"] = subject
    message["Bcc"] = bcc
    email_body = template_string
    for key, value in values_dict.items():
        email_body = email_body.replace('{{ ' + key + ' }}', str(value))
    message.attach(MIMEText(email_body, 'html'))
    return message
