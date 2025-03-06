"""
Test suite for validating file upload functionality in the FastAPI S3 application.
This module contains tests for the file validation functions, ensuring that
the correct exceptions are raised for unsupported file types and excessive file sizes.
"""
import pytest
from fastapi import UploadFile, HTTPException
from unittest.mock import MagicMock
from src.fastapi_s3_app.app.utils.validation import validate_file_type, validate_file_size, ALLOWED_FILE_TYPES, MAX_FILE_SIZE
@pytest.fixture
def mock_upload_file() -> UploadFile:
    """Fixture to create a mock UploadFile instance for testing."""
    mock_file = MagicMock(spec=UploadFile)
    mock_file.content_type = "image/jpeg"
    mock_file.file = MagicMock()
    return mock_file
class TestValidateFileType:
    """Test suite for the validate_file_type function."""
    def test_validate_file_type_valid(self, mock_upload_file: UploadFile) -> None:
        """Test that valid file types do not raise an exception.
        Scenario: When the file type is 'image/jpeg'.
        Expected outcome: No HTTPException is raised.
        """
        validate_file_type(mock_upload_file)
    def test_validate_file_type_invalid(self, mock_upload_file: UploadFile) -> None:
        """Test that invalid file types raise an HTTPException.
        Scenario: When the file type is 'application/x-zip-compressed'.
        Expected outcome: An HTTPException with a 400 status code is raised.
        Edge cases: Testing with file types not in ALLOWED_FILE_TYPES.
        """
        mock_upload_file.content_type = "application/x-zip-compressed"
        with pytest.raises(HTTPException) as exc_info:
            validate_file_type(mock_upload_file)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Unsupported file type."
@pytest.fixture
def mocked_file_size() -> UploadFile:
    """Fixture to create a mock UploadFile instance with a specific file size."""
    mock_file = MagicMock(spec=UploadFile)
    mock_file.content_type = "image/jpeg"
    mock_file.file = MagicMock()
    return mock_file
class TestValidateFileSize:
    """Test suite for the validate_file_size function."""
    def test_validate_file_size_within_limit(self, mocked_file_size: UploadFile) -> None:
        """Test that file sizes within the limit do not raise an exception.
        Scenario: When the file size is 4 MB.
        Expected outcome: No HTTPException is raised.
        """
        mocked_file_size.file.tell.return_value = 4 * 1024 * 1024  # 4 MB
        validate_file_size(mocked_file_size)
    def test_validate_file_size_exceeds_limit(self, mocked_file_size: UploadFile) -> None:
        """Test that file sizes exceeding the limit raise an HTTPException.
        Scenario: When the file size is 6 MB.
        Expected outcome: An HTTPException with a 400 status code is raised.
        Edge cases: Testing just over the allowed size.
        """
        mocked_file_size.file.tell.return_value = 6 * 1024 * 1024  # 6 MB
        with pytest.raises(HTTPException) as exc_info:
            validate_file_size(mocked_file_size)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "File size exceeds the maximum limit of 5 MB."
    def test_validate_file_size_edge_case(self, mocked_file_size: UploadFile) -> None:
        """Test that file size exactly at the limit does not raise an exception.
        Scenario: When the file size is exactly 5 MB.
        Expected outcome: No HTTPException is raised.
        """
        mocked_file_size.file.tell.return_value = 5 * 1024 * 1024  # 5 MB
        validate_file_size(mocked_file_size)
    def test_validate_file_size_empty_file(self) -> None:
        """Test that an empty file does not raise an exception.
        Scenario: When the file size is 0 MB.
        Expected outcome: No HTTPException is raised.
        """
        empty_file = MagicMock(spec=UploadFile)
        empty_file.content_type = "image/jpeg"
        empty_file.file = MagicMock()
        empty_file.file.tell.return_value = 0  # 0 MB
        validate_file_size(empty_file)
    def test_validate_file_size_mocked_file(self) -> None:
        """Test that a mocked file with specific size raises an exception.
        Scenario: When the file size is set to a mocked value exceeding the limit.
        Expected outcome: An HTTPException with a 400 status code is raised.
        """
        mocked_file = MagicMock(spec=UploadFile)
        mocked_file.content_type = "image/jpeg"
        mocked_file.file = MagicMock()
        mocked_file.file.tell.return_value = 7 * 1024 * 1024  # 7 MB
        with pytest.raises(HTTPException) as exc_info:
            validate_file_size(mocked_file)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "File size exceeds the maximum limit of 5 MB."
