import pandas as pd
from scraper import parse_file

def test_csv_parsing(tmp_path):
    csv_file = tmp_path / "employees.csv"
    csv_file.write_text(
        "Employee ID,First Name,Last Name,Email,Hire Date\n"
        "1,John,Doe,john@example.com,2020-01-01"
    )

    df = parse_file(str(csv_file))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
