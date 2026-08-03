import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv(
        "GROQ_MODEL",
        "llama-3.1-8b-instant"
    )
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_SMTP_SERVER = os.getenv(
        "MAIL_SMTP_SERVER",
        "smtp.gmail.com"
    )
    MAIL_SMTP_PORT = int(os.getenv(
        "MAIL_SMTP_PORT",
        "587"
    ))
    EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "smtp").lower()
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    MAIL_FROM = os.getenv("MAIL_FROM")


settings = Settings()
