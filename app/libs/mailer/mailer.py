import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings
from app.core.logger import logger

# Get the directory containing the current script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class Mailer:
    _host: str = None
    _port: int = None
    _from_email: str = None
    _password: str = None

    def __init__(self):
        logger.info("Initializing Mailer")
        self._host = settings.SMTP_HOST
        self._port = settings.SMTP_PORT
        self._from_email = settings.SMTP_USERNAME
        self._password = settings.SMTP_PASSWORD

    def __str__(self):
        return f"Host: {self._host}, Port: {self._port}, From: {self._from_email}, Password: {self._password}"

    async def send_mail(self, to_email: str, key):
        message = MIMEMultipart("alternative")
        message['Subject'] = "Subscription"
        message['From'] = self._from_email
        message['Cc'] = self._from_email
        message['Bcc'] = self._from_email
        message['To'] = to_email

        # Use os.path.join to create the correct path to mail.html
        mail_template_path = os.path.join(CURRENT_DIR, "mail.html")

        try:
            with open(mail_template_path, "r") as file:
                html = file.read()
        except FileNotFoundError:
            logger.error(f"Could not find mail template at: {mail_template_path}")
            raise

        logger.info(f"Using mail template: {mail_template_path}")
        html = html.replace("{{key}}", key)
        html_part = MIMEText(html, 'html')
        message.attach(html_part)

        logger.info(f"Sending mail to: {to_email}")
        smtp = smtplib.SMTP_SSL(self._host, self._port)
        status_code, response = smtp.ehlo()
        logger.info(f"Echoing the server: {status_code} {response}")

        # status_code, response = smtp.starttls()
        # print(f"[*] Starting TLS connection: {status_code} {response}")

        status_code, response = smtp.login(self._from_email, self._password)

        logger.info(f"Logging in:  {status_code} {response}")

        smtp.sendmail(self._from_email, to_email, message.as_string())

        smtp.quit()

        logger.info(f"Mail sent to: {to_email}")