from validator import validate_record

def test_valid_record():
    record = {
        "Employee ID": 1,
        "First Name": "Jane",
        "Last Name": "Doe",
        "Email": "jane@example.com",
        "Hire Date": "2021-05-10"
    }

    errors = validate_record(record)
    assert errors == []

def test_invalid_record():
    record = {
        "Employee ID": None,
        "First Name": "Jane",
        "Last Name": "",
        "Email": "invalid-email",
        "Hire Date": "10-05-2021"
    }

    errors = validate_record(record)
    assert len(errors) > 0
