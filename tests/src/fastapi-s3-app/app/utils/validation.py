"""Unit tests for file validation functions in the FastAPI S3 application.
This test suite validates the functionality of the file type and file size
validation functions to ensure they behave correctly under various scenarios.
"""
import pytest
from fastapi import UploadFile, HTTPException
from unittest.mock import MagicMock
from src.fastapi_s3_app.app.utils.validation import validate_file_type, validate_file_size, ALLOWED_FILE_TYPES, MAX_FILE_SIZE
@pytest.fixture
def mock_upload_file() -> UploadFile:
    """Fixture to create a mock UploadFile object for testing."""
    mock_file = MagicMock(spec=UploadFile)
    return mock_file
class TestValidateFileType:
    """Tests for the validate_file_type function."""
    def test_valid_file_type(self, mock_upload_file: UploadFile) -> None:
        """Test valid file type.
        Scenario: The file type is one of the allowed types.
        Expected outcome: No exception is raised.
        """
        mock_upload_file.content_type = "image/jpeg"
        validate_file_type(mock_upload_file)
    def test_invalid_file_type(self, mock_upload_file: UploadFile) -> None:
        """Test invalid file type.
        Scenario: The file type is not in the allowed types.
        Expected outcome: HTTPException is raised with status 400.
        Edge cases: Test with different invalid content types.
        """
        mock_upload_file.content_type = "text/plain"
        with pytest.raises(HTTPException) as exc_info:
            validate_file_type(mock_upload_file)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Unsupported file type."
class TestValidateFileSize:
    """Tests for the validate_file_size function."""
    @pytest.fixture
    def small_file(self, mock_upload_file: UploadFile) -> UploadFile:
        """Fixture to create a small mock UploadFile object."""
        mock_upload_file.file = MagicMock()
        mock_upload_file.file.tell.side_effect = [0, 1024]  # Simulate a file size of 1024 bytes
        return mock_upload_file
    @pytest.fixture
    def large_file(self, mock_upload_file: UploadFile) -> UploadFile:
        """Fixture to create a large mock UploadFile object."""
        mock_upload_file.file = MagicMock()
        mock_upload_file.file.tell.side_effect = [0, MAX_FILE_SIZE + 1]  # Simulate a file size exceeding the limit
        return mock_upload_file
    def test_valid_file_size(self, small_file: UploadFile) -> None:
        """Test valid file size.
        Scenario: The file size is within the allowed limit.
        Expected outcome: No exception is raised.
        """
        validate_file_size(small_file)
    def test_invalid_file_size(self, large_file: UploadFile) -> None:
        """Test invalid file size.
        Scenario: The file size exceeds the maximum limit.
        Expected outcome: HTTPException is raised with status 400.
        """
        with pytest.raises(HTTPException) as exc_info:
            validate_file_size(large_file)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "File size exceeds the maximum limit of 5 MB."
