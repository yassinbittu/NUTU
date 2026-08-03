import smtplib
import json
import traceback
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from email.message import EmailMessage

from app.config import settings


class EmailService:

    def __init__(self):

        self.provider = settings.EMAIL_PROVIDER.lower()

        print("========== EMAIL PROVIDER ==========")
        print("Provider:", self.provider)
        print("====================================")

        # -----------------------------
        # RESEND
        # -----------------------------
        if self.provider == "resend":

            if not settings.RESEND_API_KEY:
                raise ValueError(
                    "RESEND_API_KEY is missing."
                )

            if not settings.MAIL_FROM:
                raise ValueError(
                    "MAIL_FROM is missing."
                )

            return

        # -----------------------------
        # SMTP
        # -----------------------------
        if not settings.MAIL_USERNAME or not settings.MAIL_PASSWORD:
            raise ValueError(
                "MAIL_USERNAME and MAIL_PASSWORD must be set."
            )

        self.smtp_server = settings.MAIL_SMTP_SERVER
        self.smtp_port = settings.MAIL_SMTP_PORT
        self.username = settings.MAIL_USERNAME
        self.password = settings.MAIL_PASSWORD

        print("========== SMTP CONFIG ==========")
        print("SMTP Server:", self.smtp_server)
        print("SMTP Port:", self.smtp_port)
        print("Username:", self.username)
        print("Password Length:", len(self.password))
        print("=================================")

    # --------------------------------------------------
    # SEND EMAIL
    # --------------------------------------------------

    def send_email(
        self,
        subject: str,
        body: str,
        visitor_email: str | None,
        recipient_email: str,
    ) -> None:

        if self.provider == "resend":

            self._send_with_resend(
                subject=subject,
                body=body,
                visitor_email=visitor_email,
                recipient_email=recipient_email,
            )
            return

        message = EmailMessage()

        message["Subject"] = subject
        message["From"] = self.username
        message["To"] = recipient_email

        if visitor_email:
            message["Reply-To"] = visitor_email

        message.set_content(
            f"{body}\n\n"
            "---\n"
            "This message was sent by NUTU on behalf of a visitor."
        )

        try:

            print("Connecting to Gmail SMTP...")

            with smtplib.SMTP(
                self.smtp_server,
                self.smtp_port,
                timeout=30
            ) as smtp:

                smtp.ehlo()

                print("Starting TLS...")
                smtp.starttls()

                smtp.ehlo()

                print("Logging into Gmail...")
                smtp.login(
                    self.username,
                    self.password
                )

                print("Sending email...")
                smtp.send_message(message)

                print("Email sent successfully!")

        except Exception as exc:

            traceback.print_exc()

            print("EMAIL ERROR:", str(exc))

            raise

    # --------------------------------------------------
    # RESEND
    # --------------------------------------------------

    def _send_with_resend(
        self,
        subject: str,
        body: str,
        visitor_email: str | None,
        recipient_email: str,
    ) -> None:

        payload = {
            "from": settings.MAIL_FROM,
            "to": [recipient_email],
            "subject": subject,
            "text": (
                f"{body}\n\n"
                "---\n"
                "This message was sent by NUTU on behalf of a visitor."
            ),
        }

        if visitor_email:
            payload["reply_to"] = visitor_email

        request = Request(
            "https://api.resend.com/emails",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                "Content-Type": "application/json",
                "User-Agent": "NUTU/1.0",
            },
            method="POST",
        )

        try:

            print("Sending email via Resend...")

            with urlopen(request, timeout=20) as response:

                response_body = response.read().decode("utf-8")

                print("Resend Status:", response.status)
                print("Resend Response:", response_body)

                if response.status not in (200, 201):
                    raise RuntimeError(
                        f"Resend returned HTTP {response.status}"
                    )

                print("Email sent successfully using Resend!")

        except HTTPError as exc:

            details = exc.read().decode(
                "utf-8",
                errors="replace"
            )

            traceback.print_exc()

            raise RuntimeError(
                f"Resend HTTP {exc.code}: {details}"
            ) from exc

        except URLError as exc:

            traceback.print_exc()

            raise RuntimeError(
                f"Could not reach Resend: {exc.reason}"
            ) from exc


email_service = EmailService()