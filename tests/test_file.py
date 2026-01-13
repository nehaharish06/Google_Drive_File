import pytest
from scraper import parse_file

def test_invalid_file_format(tmp_path):
    invalid_file = tmp_path / "employees.txt"
    invalid_file.write_text("random text")

    with pytest.raises(Exception):
        parse_file(str(invalid_file))
