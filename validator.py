import re
from datetime import datetime

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

def validate_row(row):
    return (
        row["user_id"]
        and row["first_name"]
        and row["last_name"]
        and "@" in row["email"]
        and row["phone"].isdigit()
    )


# validator.py
def validate_record(record: dict):
    errors = []

    # Normalize keys
    normalized = {
        k.strip().lower().replace(" ", "_"): v
        for k, v in record.items()
    }

    required_fields = [
        "employee_id",
        "first_name",
        "last_name",
        "email",
        "hire_date",
    ]

    for field in required_fields:
        if field not in normalized or not normalized[field]:
            errors.append(f"{field} is missing")

    # Simple email check
    if "email" in normalized and "@" not in str(normalized["email"]):
        errors.append("invalid email")

    return errors

    