"""Test suite for file validation utilities in the FastAPI S3 application.
This module contains unit tests for the validation functions that ensure uploaded
files meet specific criteria regarding type and size.
"""
import pytest
from fastapi import UploadFile, HTTPException
from unittest.mock import MagicMock
from typing import Any
from src.fastapi_s3_app.app.utils.validation import validate_file_type, validate_file_size, ALLOWED_FILE_TYPES, MAX_FILE_SIZE
@pytest.fixture
def mock_upload_file() -> UploadFile:
    """Fixture that creates a mock UploadFile object for testing."""
    mock_file = MagicMock(spec=UploadFile)
    mock_file.file = MagicMock()
    return mock_file
class TestValidateFileType:
    """Test cases for the validate_file_type function."""
    def test_valid_file_type(self, mock_upload_file: UploadFile) -> None:
        """Test valid file types.
        Purpose: Ensure that allowed file types do not raise exceptions.
        Scenario: Validate a JPEG file type.
        Expected outcome: No exception is raised.
        """
        mock_upload_file.content_type = "image/jpeg"
        validate_file_type(mock_upload_file)
        mock_upload_file.content_type = "image/png"
        validate_file_type(mock_upload_file)
        mock_upload_file.content_type = "application/pdf"
        validate_file_type(mock_upload_file)
    def test_invalid_file_type(self, mock_upload_file: UploadFile) -> None:
        """Test invalid file types.
        Purpose: Ensure that unsupported file types raise HTTPException.
        Scenario: Validate an unsupported file type.
        Expected outcome: HTTPException is raised with the correct detail.
        Edge cases: Test types not in the ALLOWED_FILE_TYPES.
        """
        mock_upload_file.content_type = "application/x-msdownload"  # Unsupported type
        with pytest.raises(HTTPException, match="Unsupported file type."):
            validate_file_type(mock_upload_file)
class TestValidateFileSize:
    """Test cases for the validate_file_size function."""
    @pytest.fixture
    def mock_file_size(self, mock_upload_file: UploadFile) -> None:
        """Fixture to set up file size for testing."""
        mock_upload_file.file.tell.return_value = 0  # Initial position
        mock_upload_file.file.seek = MagicMock()
        yield mock_upload_file
    def test_valid_file_size(self, mock_file_size: UploadFile) -> None:
        """Test valid file sizes.
        Purpose: Ensure that file sizes within the limit do not raise exceptions.
        Scenario: Validate a file size of 4 MB.
        Expected outcome: No exception is raised.
        """
        mock_file_size.file.tell.return_value = MAX_FILE_SIZE - 1  # 4 MB
        validate_file_size(mock_file_size)
    def test_exceeding_file_size(self, mock_file_size: UploadFile) -> None:
        """Test file sizes exceeding the maximum limit.
        Purpose: Ensure that file sizes exceeding the limit raise HTTPException.
        Scenario: Validate a file size of 6 MB.
        Expected outcome: HTTPException is raised with the correct detail.
        Edge cases: Test sizes just above the limit.
        """
        mock_file_size.file.tell.return_value = MAX_FILE_SIZE + 1  # 6 MB
        with pytest.raises(HTTPException, match="File size exceeds the maximum limit of 5 MB."):
            validate_file_size(mock_file_size)
    def test_edge_case_file_size(self, mock_file_size: UploadFile) -> None:
        """Test edge case for file size validation.
        Purpose: Ensure that a file size exactly at the limit does not raise an exception.
        Scenario: Validate a file size of 5 MB.
        Expected outcome: No exception is raised.
        """
        mock_file_size.file.tell.return_value = MAX_FILE_SIZE  # Exactly 5 MB
        validate_file_size(mock_file_size)
