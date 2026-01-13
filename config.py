# config.py
from pathlib import Path

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds between retries
SUPPORTED_FORMATS = ["csv"]
DEFAULT_OUTPUT_PATH = Path("employee_data")
