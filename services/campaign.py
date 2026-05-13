import uuid
import re
import time
from datetime import datetime
from core.parser import CSVParser
from core.template import TemplateEngine
from services.attachment import AttachmentService
from providers.smtp_provider import SMTPProvider
from infra.logger import logger
from infra.database import db
from infra.config import Config


class CampaignEngine:
    def __init__(self, csv_path: str, template_str: str, campaign_name: str = None, campaign_id: int = None, rate_limit: float = None):
        self.csv_path = csv_path
        self.template_str = template_str
        self.campaign_name = campaign_name or f"Campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.campaign_id = campaign_id
        self.rate_limit = rate_limit if rate_limit is not None else Config.RATE_LIMIT
        self.accounts = Config.get_smtp_accounts()
        self.attachments = AttachmentService().load_attachments()
        logger.info(f"CampaignEngine initialized: {self.campaign_name}")

    def run(self):
        # Parse CSV
        parser = CSVParser(self.csv_path)
        recipients = parser.load()

        # Template engine
        template_engine = TemplateEngine(self.template_str)
        
        # Get subject from template (first line)
        sample_body = template_engine.render(recipients[0] if recipients else {})
        subject = sample_body.splitlines()[0] if sample_body else "No Subject"

        # Create or update campaign in DB
        if self.campaign_id:
            campaign_id = self.campaign_id
            db.update_campaign_status(campaign_id, 'running')
        else:
            campaign_id = db.create_campaign(
                self.campaign_name, 
                subject, 
                status='running',
                csv_path=self.csv_path,
                template_str=self.template_str
            )

        # Send emails with rotation
        sent_count = 0
        account_index = 0
        total_accounts = len(self.accounts)

        # Initialize SMTP provider
        logger.info(f"Connecting to SMTP account: {self.accounts[account_index]['sender_email']}")
        smtp_provider = SMTPProvider(self.accounts[account_index])
        smtp_provider.connect()
        logger.info("SMTP connected successfully")

        for i, row in enumerate(recipients):
            recipient_email = row.get("EMAIL")
            if not recipient_email:
                continue

            # SMTP Rotation
            if i > 0 and i % 10 == 0 and total_accounts > 1:
                smtp_provider.disconnect()
                account_index = (account_index + 1) % total_accounts
                smtp_provider = SMTPProvider(self.accounts[account_index])
                smtp_provider.connect()
                logger.info(f"Switched to SMTP account: {self.accounts[account_index]['sender_email']}")

            try:
                # Generate unique recipient ID for tracking
                recipient_id = str(uuid.uuid4())
                
                db.add_recipient(recipient_id, campaign_id, recipient_email, subject_used=subject)

                # Render body
                body = template_engine.render(row)
                
                # Wrap links for click tracking
                def wrap_link(match):
                    url = match.group(1)
                    return f'href="{Config.APP_URL}/api/track/click/{recipient_id}?url={url}"'
                
                body = re.sub(r'href="([^"]+)"', wrap_link, body)

                # Inject tracking pixel
                tracking_pixel = f'<img src="{Config.APP_URL}/api/track/open/{recipient_id}" width="1" height="1" style="display:none;" />'
                body += f"\n\n{tracking_pixel}"

                success = smtp_provider.send_email(
                    to_email=recipient_email,
                    subject=subject,
                    body=body,
                    attachments=self.attachments
                )

                if success:
                    sent_count += 1
                    db.update_recipient_status(recipient_id, "sent", datetime.now().isoformat())
                else:
                    db.update_recipient_status(recipient_id, "failed")

                # Smart Rate Limiting
                time.sleep(self.rate_limit)

            except Exception as e:
                logger.error(f"Failed to process recipient {recipient_email}: {e}")

        logger.info(f"Campaign finished. Total emails sent: {sent_count}")
        db.update_campaign_status(campaign_id, 'completed')

        # Disconnect last SMTP
        smtp_provider.disconnect()