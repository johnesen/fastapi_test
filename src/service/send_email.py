import random

from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from config.settings import (
    MAIL_FROM,
    MAIL_FROM_NAME,
    MAIL_PASSWORD,
    MAIL_PORT,
    MAIL_SERVER,
    MAIL_USERNAME,
)

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)
fm = FastMail(conf)


class SendEmailService:
    @classmethod
    async def send_email(cls, email_to: str, body: str, subject: str):
        message = MessageSchema(
            subject=subject, recipients=[email_to], body=body, subtype="html"
        )

        await fm.send_message(message)

    @staticmethod
    async def generate_code():
        digit = str(random.randint(1, 999_999))
        code = digit if len(digit) == 6 else "0" * (6 - len(digit)) + digit
        return code

    @classmethod
    def send_email_background(
        cls, background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict
    ):
        message = MessageSchema(
            subject=subject, recipients=[email_to], body=body, subtype="html"
        )
        background_tasks.add_task(fm.send_message, message)
