from unittest.mock import patch, Mock
from scraper import download_file

@patch("requests.get")
def test_file_download_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"Employee ID,First Name,Last Name,Email,Hire Date"
    mock_response.headers = {"Content-Type": "text/csv"}

    mock_get.return_value = mock_response

    file_path = download_file("fake_url")
    assert file_path.endswith(".csv")
