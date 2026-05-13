import time
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown

from infra.config import Config
from infra.logger import logger


class SMTPProvider:
    def __init__(self, account=None):
        self.server = None
        # Use provided account or default from Config
        if account:
            self.display_name = account.get("display_name", Config.DISPLAY_NAME)
            self.sender_email = account.get("sender_email", Config.SENDER_EMAIL)
            self.password = account.get("password", Config.PASSWORD)
            self.smtp_host = account.get("smtp_host", Config.SMTP_HOST)
            self.smtp_port = int(account.get("smtp_port", Config.SMTP_PORT))
        else:
            self.display_name = Config.DISPLAY_NAME
            self.sender_email = Config.SENDER_EMAIL
            self.password = Config.PASSWORD
            self.smtp_host = Config.SMTP_HOST
            self.smtp_port = Config.SMTP_PORT

    def connect(self):
        try:
            self.server = SMTP(self.smtp_host, self.smtp_port)
            self.server.ehlo()
            self.server.starttls()
            self.server.login(self.sender_email, self.password)

            logger.info(f"SMTP connection established for {self.sender_email}")

        except Exception as e:
            logger.error(f"SMTP connection failed for {self.sender_email}: {e}")
            raise

    def disconnect(self):
        if self.server:
            try:
                self.server.quit()
            except:
                pass
            logger.info(f"SMTP connection closed for {self.sender_email}")

    def send_email(self, to_email: str, subject: str, body: str, attachments=None):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{self.display_name} <{self.sender_email}>"
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
                    self.sender_email,
                    to_email,
                    msg.as_string()
                )

                logger.info(f"Email sent to {to_email} via {self.sender_email}")
                time.sleep(Config.RATE_LIMIT)
                return True

            except Exception as e:
                logger.warning(
                    f"Retry {attempt + 1}/{Config.RETRY_COUNT} failed for {to_email} via {self.sender_email}: {e}"
                )
                time.sleep(2 ** attempt)

        logger.error(f"Failed to send email to {to_email} after retries via {self.sender_email}")
        return False