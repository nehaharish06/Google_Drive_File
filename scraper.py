import os
import time
import requests
import pandas as pd
from logger import logger
from config import MAX_RETRIES, SUPPORTED_FORMATS
from validator import validate_record

def download_file(url: str, output_path="employee_data"):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Attempt {attempt} downloading file...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")
            ext = "csv" if "csv" in content_type else "xlsx"

            file_path = f"{output_path}.{ext}"
            with open(file_path, "wb") as f:
                f.write(response.content)

            logger.info("Download successful")
            return file_path

        except Exception as e:
            logger.error(f"Download failed: {e}")
            time.sleep(2)

    raise Exception("File download failed after retries")

def parse_file(file_path: str) -> pd.DataFrame:
    ext = file_path.split(".")[-1]

    if ext not in SUPPORTED_FORMATS:
        raise ValueError("Unsupported file format")

    if ext == "csv":
        return pd.read_csv(file_path)
    else:
        return pd.read_excel(file_path)

def process_employee_data(df: pd.DataFrame):
    valid_records = []
    invalid_records = []

    for _, row in df.iterrows():
        record = row.to_dict()
        errors = validate_record(record)

        if errors:
            invalid_records.append({"record": record, "errors": errors})
        else:
            valid_records.append(record)

    logger.info(f"Valid records: {len(valid_records)}")
    logger.info(f"Invalid records: {len(invalid_records)}")

    return valid_records, invalid_records
