import re
from datetime import datetime

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

REQUIRED_FIELDS = [
    "Employee ID",
    "First Name",
    "Last Name",
    "Email",
    "Hire Date"
]

def validate_record(record: dict) -> list:
    errors = []

    for field in REQUIRED_FIELDS:
        if not record.get(field):
            errors.append(f"Missing field: {field}")

    if record.get("Email") and not re.match(EMAIL_REGEX, record["Email"]):
        errors.append("Invalid email format")

    if record.get("Hire Date"):
        try:
            datetime.strptime(record["Hire Date"], "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid hire date format")

    return errors
