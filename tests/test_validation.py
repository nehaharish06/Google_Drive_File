from validator import validate_record

def test_valid_record():
    record = {
        "Employee ID": 1,
        "First Name": "Jane",
        "Last Name": "Doe",
        "Email": "jane@example.com",
        "Date of Birth": "1976-05-10"
    }

    errors = validate_record(record)
    assert errors == []

def test_invalid_record():
    record = {
        "Employee ID": None,
        "First Name": "Jane",
        "Last Name": "",
        "Email": "invalid-email",
        "Date of Birth": "10-05-1976"
    }

    errors = validate_record(record)
    assert len(errors) > 0
