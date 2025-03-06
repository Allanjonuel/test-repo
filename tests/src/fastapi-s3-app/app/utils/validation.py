"""Unit tests for file validation functions in the FastAPI S3 application.
This test suite covers the validation of file types and sizes for uploaded files,
ensuring that only allowed file types are accepted and that file sizes do not exceed
the defined maximum limit.
"""
import pytest
from fastapi import UploadFile, HTTPException
from unittest.mock import MagicMock
from src.fastapi_s3_app.app.utils.validation import validate_file_type, validate_file_size, ALLOWED_FILE_TYPES, MAX_FILE_SIZE
@pytest.fixture
def mock_upload_file() -> UploadFile:
    """Fixture to create a mock UploadFile object for testing."""
    file_mock = MagicMock(spec=UploadFile)
    file_mock.file = MagicMock()
    return file_mock
class TestValidateFileType:
    """Test suite for the validate_file_type function."""
    def test_valid_file_type_jpeg(self, mock_upload_file: UploadFile) -> None:
        """Test valid JPEG file type.
        Scenario: A JPEG file is uploaded.
        Expected outcome: No exception is raised.
        """
        mock_upload_file.content_type = "image/jpeg"
        validate_file_type(mock_upload_file)
    def test_valid_file_type_png(self, mock_upload_file: UploadFile) -> None:
        """Test valid PNG file type.
        Scenario: A PNG file is uploaded.
        Expected outcome: No exception is raised.
        """
        mock_upload_file.content_type = "image/png"
        validate_file_type(mock_upload_file)
    def test_valid_file_type_pdf(self, mock_upload_file: UploadFile) -> None:
        """Test valid PDF file type.
        Scenario: A PDF file is uploaded.
        Expected outcome: No exception is raised.
        """
        mock_upload_file.content_type = "application/pdf"
        validate_file_type(mock_upload_file)
    def test_invalid_file_type(self, mock_upload_file: UploadFile) -> None:
        """Test invalid file type.
        Scenario: An unsupported file type is uploaded.
        Expected outcome: HTTPException is raised with status code 400.
        """
        mock_upload_file.content_type = "text/plain"
        with pytest.raises(HTTPException) as exc_info:
            validate_file_type(mock_upload_file)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Unsupported file type."
class TestValidateFileSize:
    """Test suite for the validate_file_size function."""
    def test_valid_file_size(self, mock_upload_file: UploadFile) -> None:
        """Test valid file size.
        Scenario: A file size is within the allowed limit (less than 5 MB).
        Expected outcome: No exception is raised.
        """
        mock_upload_file.file.tell.return_value = MAX_FILE_SIZE - 1  # Set size to 4.999 MB
        mock_upload_file.file.seek = MagicMock()  # Mock seek method
        validate_file_size(mock_upload_file)
    def test_exceeding_file_size(self, mock_upload_file: UploadFile) -> None:
        """Test exceeding file size.
        Scenario: A file size exceeds the maximum limit (greater than 5 MB).
        Expected outcome: HTTPException is raised with status code 400.
        """
        mock_upload_file.file.tell.return_value = MAX_FILE_SIZE + 1  # Set size to 5.001 MB
        mock_upload_file.file.seek = MagicMock()  # Mock seek method
        with pytest.raises(HTTPException) as exc_info:
            validate_file_size(mock_upload_file)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "File size exceeds the maximum limit of 5 MB."
    def test_zero_file_size(self, mock_upload_file: UploadFile) -> None:
        """Test zero file size.
        Scenario: An empty file is uploaded.
        Expected outcome: No exception is raised.
        """
        mock_upload_file.file.tell.return_value = 0  # Set size to 0 bytes
        mock_upload_file.file.seek = MagicMock()  # Mock seek method
        validate_file_size(mock_upload_file)
    def test_file_size_boundary(self, mock_upload_file: UploadFile) -> None:
        """Test file size at the boundary limit.
        Scenario: A file size exactly at the maximum limit (5 MB).
        Expected outcome: No exception is raised.
        """
        mock_upload_file.file.tell.return_value = MAX_FILE_SIZE  # Set size to 5 MB
        mock_upload_file.file.seek = MagicMock()  # Mock seek method
        validate_file_size(mock_upload_file)
