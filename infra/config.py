import os
import json
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
    APP_URL = os.getenv("APP_URL", "http://localhost:8000")

    @staticmethod
    def get_smtp_accounts():
        """Returns a list of SMTP account dictionaries."""
        accounts_file = "data/smtp_accounts.json"
        if os.path.exists(accounts_file):
            try:
                with open(accounts_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Default to .env if no file exists
        return [{
            "display_name": Config.DISPLAY_NAME,
            "sender_email": Config.SENDER_EMAIL,
            "password": Config.PASSWORD,
            "smtp_host": Config.SMTP_HOST,
            "smtp_port": Config.SMTP_PORT
        }]

    @staticmethod
    def validate():
        missing = []

        if not Config.SENDER_EMAIL:
            missing.append("SENDER_EMAIL")
        if not Config.PASSWORD:
            missing.append("PASSWORD")

        if missing:
            raise ValueError(f"Missing required env variables: {', '.join(missing)}")