from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

async def send_email(to, subject, body):
    message = MessageSchema(
        subject=subject,
        recipients=[to],
        body=body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)