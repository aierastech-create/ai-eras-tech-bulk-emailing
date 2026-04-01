import os
from typing import List
from email.mime.base import MIMEBase
from email import encoders
from infra.logger import logger


class AttachmentService:
    def __init__(self, folder_path: str = "attachments"):
        self.folder_path = folder_path

    def load_attachments(self) -> List[MIMEBase]:
        attachments = []

        if not os.path.exists(self.folder_path):
            logger.warning("No attachments folder found")
            return attachments

        for filename in os.listdir(self.folder_path):
            filepath = os.path.join(self.folder_path, filename)

            try:
                with open(filepath, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())

                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{filename}"'
                )

                attachments.append(part)
                logger.info(f"Loaded attachment: {filename}")

            except Exception as e:
                logger.error(f"Failed to load attachment {filename}: {e}")

        return attachments