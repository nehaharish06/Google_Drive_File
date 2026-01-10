# scraper.py
import time
import requests
import pandas as pd
from config import MAX_RETRIES, RETRY_DELAY, SUPPORTED_FORMATS, DEFAULT_OUTPUT_PATH
from logger import logger
from validator import validate_record

def download_file(url: str, output_path=None):
    output_path = output_path or DEFAULT_OUTPUT_PATH
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

            logger.info(f"Download successful: {file_path}")
            return file_path

        except Exception as e:
            logger.error(f"Download failed: {e}")
            if attempt < MAX_RETRIES:
                logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                raise Exception("File download failed after retries")

def parse_file(file_path: str) -> pd.DataFrame:
    ext = file_path.split(".")[-1].lower()

    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported file format: {ext}")

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


if __name__ == "__main__":
    URL = "https://drive.google.com/uc?id=1AWPf-pJodJKeHsARQK_RHiNsE8fjPCVK&export=download"

    try:
        file_path = download_file(URL)
        df = parse_file(file_path)
        valid, invalid = process_employee_data(df)

        logger.info("Sample valid records:")
        for record in valid[:5]:
            logger.info(record)

    except Exception as e:
        logger.critical(f"Scraper failed: {e}")
