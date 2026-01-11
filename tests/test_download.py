from unittest.mock import patch, Mock
from scraper import download_file
import os

@patch("scraper.requests.get")  # IMPORTANT: patch where it's USED
def test_file_download_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = (
        b"Employee ID,First Name,Last Name,Email,Job Title,Phone Number,Hire Date\n"
        b"1,John,Doe,john@example.com,Engineer,9999999999,2022-01-01\n"
        b"2,Jane,Smith,jane@example.com,Manager,8888888888,2021-06-15\n"
    )
    mock_response.headers = {"Content-Type": "text/csv"}
    mock_response.raise_for_status = Mock()

    mock_get.return_value = mock_response

    file_path = download_file("fake_url")

    # File exists
    assert os.path.exists(file_path)

    #  Correct extension
    assert file_path.endswith(".csv")

    #  Entire content downloaded
    with open(file_path, "rb") as f:
        content = f.read()

    assert b"John,Doe" in content
    assert b"Jane,Smith" in content

    # Cleanup
    os.remove(file_path)
