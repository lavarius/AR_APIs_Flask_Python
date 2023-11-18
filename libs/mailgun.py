import requests
from typing import List
from requests import Response, post


import os
from dotenv import load_dotenv

load_dotenv()



class Mailgun:
    MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
    MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
    FROM_TITLE = os.getenv("FROM_TITLE")
    FROM_EMAIL = os.getenv("FROM_EMAIL")
    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str) -> Response:

        return requests.post(
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