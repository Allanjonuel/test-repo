"""Unit tests for the validation functions in the FastAPI S3 application.
This module contains unit tests for the file validation functions, ensuring that
the file type and size are validated correctly according to the specified rules.
"""
import pytest
from fastapi import UploadFile, HTTPException
from unittest.mock import MagicMock
from typing import Any
from src.fastapi_s3_app.app.utils.validation import validate_file_type, validate_file_size, ALLOWED_FILE_TYPES, MAX_FILE_SIZE
@pytest.fixture
def mock_upload_file() -> UploadFile:
    """Fixture to create a mock UploadFile object for testing.
    Returns:
        UploadFile: A mock UploadFile instance.
    """
    mock_file = MagicMock(spec=UploadFile)
    mock_file.file = MagicMock()
    return mock_file
class TestValidateFileType:
    """Test suite for the validate_file_type function."""
    def test_valid_file_type(self, mock_upload_file: UploadFile) -> None:
        """Test that a valid file type does not raise an exception.
        Purpose: Ensure that the function allows valid file types.
        Scenario: Given a file with a content type of 'image/jpeg'.
        Expected outcome: No exception should be raised.
        """
        mock_upload_file.content_type = 'image/jpeg'
        validate_file_type(mock_upload_file)
    def test_invalid_file_type(self, mock_upload_file: UploadFile) -> None:
        """Test that an invalid file type raises an HTTPException.
        Purpose: Ensure that the function raises an exception for invalid file types.
        Scenario: Given a file with a content type of 'application/zip'.
        Expected outcome: An HTTPException should be raised with a 400 status code.
        """
        mock_upload_file.content_type = 'application/zip'
        with pytest.raises(HTTPException) as excinfo:
            validate_file_type(mock_upload_file)
        assert excinfo.value.status_code == 400
        assert excinfo.value.detail == "Unsupported file type."
class TestValidateFileSize:
    """Test suite for the validate_file_size function."""
    def test_valid_file_size(self, mock_upload_file: UploadFile) -> None:
        """Test that a valid file size does not raise an exception.
        Purpose: Ensure that the function allows file sizes within the limit.
        Scenario: Given a file size of 4 MB.
        Expected outcome: No exception should be raised.
        """
        mock_upload_file.file.tell.return_value = 4 * 1024 * 1024  # 4 MB
        validate_file_size(mock_upload_file)
    def test_exceeding_file_size(self, mock_upload_file: UploadFile) -> None:
        """Test that exceeding file size raises an HTTPException.
        Purpose: Ensure that the function raises an exception for oversized files.
        Scenario: Given a file size of 6 MB.
        Expected outcome: An HTTPException should be raised with a 400 status code.
        """
        mock_upload_file.file.tell.return_value = 6 * 1024 * 1024  # 6 MB
        with pytest.raises(HTTPException) as excinfo:
            validate_file_size(mock_upload_file)
        assert excinfo.value.status_code == 400
        assert excinfo.value.detail == "File size exceeds the maximum limit of 5 MB."
    def test_edge_case_zero_file_size(self, mock_upload_file: UploadFile) -> None:
        """Test that a file size of zero does not raise an exception.
        Purpose: Ensure that the function allows zero file size, representing an empty file.
        Scenario: Given a file size of 0 bytes.
        Expected outcome: No exception should be raised.
        """
        mock_upload_file.file.tell.return_value = 0  # 0 bytes
        validate_file_size(mock_upload_file)
    def test_edge_case_max_file_size(self, mock_upload_file: UploadFile) -> None:
        """Test that a file size equal to the maximum limit does not raise an exception.
        Purpose: Ensure that the function allows files at the maximum size limit.
        Scenario: Given a file size of exactly 5 MB.
        Expected outcome: No exception should be raised.
        """
        mock_upload_file.file.tell.return_value = MAX_FILE_SIZE  # 5 MB
        validate_file_size(mock_upload_file)
    def test_edge_case_just_over_max_file_size(self, mock_upload_file: UploadFile) -> None:
        """Test that a file size just over the maximum limit raises an HTTPException.
        Purpose: Ensure that the function raises an exception for files just over the limit.
        Scenario: Given a file size of 5.1 MB.
        Expected outcome: An HTTPException should be raised with a 400 status code.
        """
        mock_upload_file.file.tell.return_value = MAX_FILE_SIZE + 100 * 1024  # 5.1 MB
        with pytest.raises(HTTPException) as excinfo:
            validate_file_size(mock_upload_file)
        assert excinfo.value.status_code == 400
        assert excinfo.value.detail == "File size exceeds the maximum limit of 5 MB."
