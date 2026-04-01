import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Email identity
    DISPLAY_NAME = os.getenv("DISPLAY_NAME")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    # SMTP Config
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

    # Engine behavior
    RATE_LIMIT = float(os.getenv("RATE_LIMIT", 1))  # seconds between emails
    RETRY_COUNT = int(os.getenv("RETRY_COUNT", 3))

    @staticmethod
    def validate():
        missing = []

        if not Config.SENDER_EMAIL:
            missing.append("SENDER_EMAIL")
        if not Config.PASSWORD:
            missing.append("PASSWORD")

        if missing:
            raise ValueError(f"Missing required env variables: {', '.join(missing)}")