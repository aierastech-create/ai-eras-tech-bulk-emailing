from core.parser import CSVParser
from core.template import TemplateEngine
from services.attachment import AttachmentService
from providers.smtp_provider import SMTPProvider
from infra.logger import logger


class CampaignEngine:
    def __init__(self, csv_path: str, template_str: str):
        self.csv_path = csv_path
        self.template_str = template_str
        self.smtp_provider = SMTPProvider()
        self.attachments = AttachmentService().load_attachments()

    def run(self):
        # Connect SMTP
        self.smtp_provider.connect()

        # Parse CSV
        parser = CSVParser(self.csv_path)
        recipients = parser.load()

        # Template engine
        template_engine = TemplateEngine(self.template_str)

        # Send emails
        sent_count = 0
        for row in recipients:
            try:
                body = template_engine.render(row)
                subject = body.splitlines()[0] if body else "No Subject"

                success = self.smtp_provider.send_email(
                    to_email=row["EMAIL"],
                    subject=subject,
                    body=body,
                    attachments=self.attachments
                )

                if success:
                    sent_count += 1

            except Exception as e:
                logger.error(f"Failed to process recipient {row.get('EMAIL')}: {e}")

        logger.info(f"Campaign finished. Total emails sent: {sent_count}")

        # Disconnect SMTP
        self.smtp_provider.disconnect()