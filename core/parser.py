import csv
from typing import List, Dict
from infra.logger import logger


class CSVParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> List[Dict]:
        try:
            with open(self.file_path, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                data = list(reader)

                if not data:
                    raise ValueError("CSV file is empty")

                if "EMAIL" not in reader.fieldnames:
                    raise ValueError("CSV must contain 'EMAIL' column")

                logger.info(f"Loaded {len(data)} records from CSV")
                return data

        except FileNotFoundError:
            logger.error(f"CSV file not found: {self.file_path}")
            raise

        except Exception as e:
            logger.error(f"Error reading CSV: {e}")
            raise