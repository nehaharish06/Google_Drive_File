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
            logger.info(f"Attempt {attempt} downloading CSV file...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            file_path = f"{output_path}.csv"
            with open(file_path, "wb") as f:
                f.write(response.content)

            logger.info(f"Download successful: {file_path}")
            return file_path

        except Exception as e:
            logger.error(f"Download failed: {e}")
            time.sleep(RETRY_DELAY)

    raise Exception("CSV download failed after retries")


def parse_file(file_path: str) -> pd.DataFrame:
    ext = file_path.split(".")[-1].lower()

    if ext == "csv":
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # Normalize columns
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    COLUMN_MAPPING = {
        "user_id": "Employee ID",
        "first_name": "First Name",
        "last_name": "Last Name",
        "email": "Email",
        "phone": "Phone Number",
        "date_of_birth": "Hire Date",
        "job_title": "Job Title",
    }

    df.rename(columns=COLUMN_MAPPING, inplace=True)

    logger.info(f"CSV Columns after mapping: {list(df.columns)}")
    return df



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
    logger.info(f"CSV Columns: {list(df.columns)}")


    return valid_records, invalid_records

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


if __name__ == "__main__":
    URL = "https://drive.google.com/uc?id=1AWPf-pJodJKeHsARQK_RHiNsE8fjPCVK&export=download"

    try:
        file_path = download_file(URL)
        df = parse_file(file_path)
        df = normalize_columns(df)
        valid, invalid = process_employee_data(df)

        logger.info("Sample valid records:")
        for record in valid[:5]:
            logger.info(record)

    except Exception as e:
        logger.critical(f"Scraper failed: {e}")
