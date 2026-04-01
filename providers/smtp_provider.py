import time
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown

from infra.config import Config
from infra.logger import logger


class SMTPProvider:
    def __init__(self):
        self.server = None

    def connect(self):
        try:
            self.server = SMTP(Config.SMTP_HOST, Config.SMTP_PORT)
            self.server.ehlo()
            self.server.starttls()
            self.server.login(Config.SENDER_EMAIL, Config.PASSWORD)

            logger.info("SMTP connection established")

        except Exception as e:
            logger.error(f"SMTP connection failed: {e}")
            raise

    def disconnect(self):
        if self.server:
            self.server.quit()
            logger.info("SMTP connection closed")

    def send_email(self, to_email: str, subject: str, body: str, attachments=None):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{Config.DISPLAY_NAME} <{Config.SENDER_EMAIL}>"
        msg["To"] = to_email

        # Plain + HTML
        html = markdown.markdown(body)

        part1 = MIMEText(body, "plain")
        part2 = MIMEText(html, "html")

        msg.attach(part1)
        msg.attach(part2)

        # Attachments
        if attachments:
            for attachment in attachments:
                msg.attach(attachment)

        # Retry logic
        for attempt in range(Config.RETRY_COUNT):
            try:
                self.server.sendmail(
                    Config.SENDER_EMAIL,
                    to_email,
                    msg.as_string()
                )

                logger.info(f"Email sent to {to_email}")
                time.sleep(Config.RATE_LIMIT)
                return True

            except Exception as e:
                logger.warning(
                    f"Retry {attempt + 1}/{Config.RETRY_COUNT} failed for {to_email}: {e}"
                )
                time.sleep(2 ** attempt)

        logger.error(f"Failed to send email to {to_email} after retries")
        return False