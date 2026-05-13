import argparse
import sys
import os

# Fix for ModuleNotFoundError when running from subdirectories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.campaign import CampaignEngine
from infra.logger import logger
from infra.config import Config


def main():
    parser = argparse.ArgumentParser(
        description="MailForge - Bulk Email Automation & Campaign Engine"
    )
    parser.add_argument(
        "--csv", required=True, help="Path to CSV file containing recipients"
    )
    parser.add_argument(
        "--template", required=True, help="Path to Markdown template file"
    )

    args = parser.parse_args()

    try:
        # Validate configuration before starting
        Config.validate()

        with open(args.template, "r", encoding="utf-8") as f:
            template_str = f.read()

        engine = CampaignEngine(csv_path=args.csv, template_str=template_str)
        engine.run()

    except Exception as e:
        logger.error(f"Error running campaign: {e}")


if __name__ == "__main__":
    main()