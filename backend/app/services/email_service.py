import smtplib
from email.message import EmailMessage

from app.config import settings


class EmailService:

    def __init__(self):

        if not settings.MAIL_USERNAME or not settings.MAIL_PASSWORD:
            raise ValueError(
                "MAIL_USERNAME and MAIL_PASSWORD must be set in the environment."
            )

        self.smtp_server = settings.MAIL_SMTP_SERVER
        self.smtp_port = settings.MAIL_SMTP_PORT
        self.username = settings.MAIL_USERNAME
        self.password = settings.MAIL_PASSWORD

    def send_email(
        self,
        subject: str,
        body: str,
        visitor_email: str | None,
        recipient_email: str,
    ) -> None:

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = self.username
        message["To"] = recipient_email
        if visitor_email:
            message["Reply-To"] = visitor_email

        message.set_content(
            f"{body}\n\n"
            f"---\n"
            "This message was sent by NUTU on behalf of a visitor."
        )

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
            smtp.starttls()
            smtp.login(self.username, self.password)
            smtp.send_message(message)


email_service = EmailService()
