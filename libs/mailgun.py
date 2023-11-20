import requests
from typing import List
from requests import Response, post


import os
from dotenv import load_dotenv

load_dotenv()

FAILED_LOAD_API_KEY = "Failed to load Mailgun API Key."
FAILED_LOAD_DOMAIN = "Failed to load Mailgun Domain."
ERROR_SENDING_EMAIL = "Error in sending confirmation email, user registration failed."

class MailgunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:
    MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN") # can be None
    MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY") # can be None
    FROM_TITLE = os.getenv("FROM_TITLE")
    FROM_EMAIL = os.getenv("FROM_EMAIL")
    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise MailgunException(FAILED_LOAD_API_KEY)
        if cls.MAILGUN_DOMAIN is None:
            raise MailgunException(FAILED_LOAD_DOMAIN)
        response = requests.post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )
        if response.status_code != 200:
            raise MailgunException(ERROR_SENDING_EMAIL)
        
        return response