import pandas as pd
from scraper import parse_file

def test_validate_data_structure(tmp_path):
    """
    Test Case 4: Validate Data Structure
    """

    csv_content = """index,user_id,first_name,last_name,sex,email,phone,date_of_birth,job_title
1,EMP001,Jane,Doe,Female,jane@example.com,9876543210,1976-05-10,Developer
"""

    csv_file = tmp_path / "employee_data.csv"
    csv_file.write_text(csv_content)

    df = parse_file(str(csv_file))

    expected_columns = {
        "index",
        "Employee ID",
        "First Name",
        "Last Name",
        "sex",
        "Email",
        "Phone Number",
        "Date of Birth",
        "Job Title",
    }

    # Validate mapped structure (parse stage)
    assert set(df.columns) == expected_columns

    # Data accessibility checks
    assert isinstance(df.loc[0, "Employee ID"], str)
    assert isinstance(df.loc[0, "Email"], str)
