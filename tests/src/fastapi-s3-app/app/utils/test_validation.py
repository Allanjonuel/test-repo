"""Test suite for the validation utilities in the FastAPI S3 application.
This module contains unit tests for the file validation functions, ensuring that
uploaded files meet the specified type and size requirements. Tests cover both
valid and invalid scenarios, including edge cases and error handling.
"""
import pytest
from fastapi import UploadFile, HTTPException
from unittest.mock import MagicMock
from typing import Any
from src.fastapi_s3_app.app.utils.validation import validate_file_type, validate_file_size, ALLOWED_FILE_TYPES, MAX_FILE_SIZE
@pytest.fixture
def mock_upload_file() -> UploadFile:
    """Fixture to create a mock UploadFile object."""
    mock_file = MagicMock(spec=UploadFile)
    mock_file.file = MagicMock()
    return mock_file
class TestValidateFileType:
    """Test suite for the validate_file_type function."""
    def test_valid_file_type(self, mock_upload_file: UploadFile) -> None:
        """Test that a valid file type does not raise an exception.
        Scenario: The file type is one of the allowed types (e.g., JPEG).
        Expected outcome: No exception is raised.
        """
        mock_upload_file.content_type = "image/jpeg"
        try:
            validate_file_type(mock_upload_file)
        except HTTPException:
            pytest.fail("HTTPException raised for valid file type.")
    def test_invalid_file_type(self, mock_upload_file: UploadFile) -> None:
        """Test that an invalid file type raises an HTTPException.
        Scenario: The file type is not in the allowed types (e.g., TXT).
        Expected outcome: An HTTPException is raised with a 400 status code.
        """
        mock_upload_file.content_type = "text/plain"
        with pytest.raises(HTTPException) as exc_info:
            validate_file_type(mock_upload_file)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Unsupported file type."
class TestValidateFileSize:
    """Test suite for the validate_file_size function."""
    def test_valid_file_size(self, mock_upload_file: UploadFile) -> None:
        """Test that a valid file size does not raise an exception.
        Scenario: The file size is within the allowed limit (e.g., 4 MB).
        Expected outcome: No exception is raised.
        """
        mock_upload_file.file.tell.return_value = 4 * 1024 * 1024  # 4 MB
        validate_file_size(mock_upload_file)  # Should not raise
    def test_exceeding_file_size(self, mock_upload_file: UploadFile) -> None:
        """Test that exceeding file size raises an HTTPException.
        Scenario: The file size exceeds the maximum limit (e.g., 6 MB).
        Expected outcome: An HTTPException is raised with a 400 status code.
        """
        mock_upload_file.file.tell.return_value = 6 * 1024 * 1024  # 6 MB
        with pytest.raises(HTTPException) as exc_info:
            validate_file_size(mock_upload_file)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "File size exceeds the maximum limit of 5 MB."
    def test_edge_case_exact_file_size(self, mock_upload_file: UploadFile) -> None:
        """Test that the exact maximum file size does not raise an exception.
        Scenario: The file size is exactly at the maximum limit (5 MB).
        Expected outcome: No exception is raised.
        """
        mock_upload_file.file.tell.return_value = MAX_FILE_SIZE  # 5 MB
        validate_file_size(mock_upload_file)  # Should not raise
    def test_zero_file_size(self, mock_upload_file: UploadFile) -> None:
        """Test that a file with zero size does not raise an exception.
        Scenario: The file size is zero bytes.
        Expected outcome: No exception is raised.
        """
        mock_upload_file.file.tell.return_value = 0  # 0 MB
        validate_file_size(mock_upload_file)  # Should not raise
    def test_negative_file_size(self, mock_upload_file: UploadFile) -> None:
        """Test that a negative file size raises an HTTPException.
        Scenario: The file size is set to a negative value.
        Expected outcome: An HTTPException is raised with a 400 status code.
        """
        mock_upload_file.file.tell.return_value = -1  # Invalid size
        with pytest.raises(HTTPException) as exc_info:
            validate_file_size(mock_upload_file)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "File size exceeds the maximum limit of 5 MB."
