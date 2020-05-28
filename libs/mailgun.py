import os
from typing import List
from requests import Response, post


class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message


class Mailgun:
    FROM_TITLE = 'Pricing service'
    FROM_EMAIL = 'do-not-reply@sandbox24639b17bc944645b423a3404a88ced1.mailgun.org'

    @classmethod
    def send_mail(cls, email:  List[str], subject: str, text: str, html: str) -> Response:        
        api_key = os.environ.get('MAILGUN_API_KEY', None)
        domain = os.environ.get('MAILGUN_DOMAIN', None)

        if api_key is None:
            raise MailgunException('Failed to load Mailgun API key.')

        if domain is None:
            raise MailgunException('Failed to load Mailgun domain.')

        response = post(f"{domain}/messages",
                        auth=("api", api_key),
                        data={"from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                              "to": email,
                              "subject": subject,
                              "text": text,
                              "html": html})
        if response != 200:
            raise MailgunException('An error occured while sending e-mail.')
        
        return response
