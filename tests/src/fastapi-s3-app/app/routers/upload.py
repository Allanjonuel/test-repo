"""Test suite for the upload module in the FastAPI S3 application.
This module contains tests for the file upload functionality, ensuring that
files are correctly validated and uploaded to the S3 service, and that
appropriate HTTP responses are returned based on various conditions.
"""
import pytest
from typing import Any, Dict
from fastapi import UploadFile
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.fastapi_s3_app.app.routers.upload import router
@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """Fixture to create a FastAPI test client for the upload router."""
    return TestClient(router)
@pytest.fixture
def mock_s3_service() -> Any:
    """Fixture to mock the S3Service for testing file uploads."""
    with patch("src.fastapi_s3_app.app.routers.upload.S3Service") as mock:
        yield mock
@pytest.fixture
def mock_validate_file_type() -> Any:
    """Fixture to mock the validate_file_type function."""
    with patch("src.fastapi_s3_app.app.routers.upload.validate_file_type") as mock:
        yield mock
@pytest.fixture
def mock_validate_file_size() -> Any:
    """Fixture to mock the validate_file_size function."""
    with patch("src.fastapi_s3_app.app.routers.upload.validate_file_size") as mock:
        yield mock
@pytest.fixture
def upload_file() -> UploadFile:
    """Fixture to create a mock UploadFile object."""
    file_mock = MagicMock(spec=UploadFile)
    file_mock.filename = "test_file.txt"
    file_mock.content_type = "text/plain"
    file_mock.file = MagicMock()  # Mock the file stream
    return file_mock
class TestUploadFile:
    """Test cases for the upload_file endpoint."""
    def test_successful_upload(self, test_client: TestClient, mock_s3_service: Any,
                                mock_validate_file_type: Any, mock_validate_file_size: Any,
                                upload_file: UploadFile) -> None:
        """Test successful file upload to S3.
        Purpose: Validate that the file is uploaded successfully.
        Scenario: A valid file is provided, and the S3 service is mocked
        to return a file URL.
        Expected outcome: A 200 response with a success message and file URL.
        """
        mock_validate_file_type.return_value = None
        mock_validate_file_size.return_value = None
        mock_s3_service.return_value.upload_file_to_s3.return_value = "http://s3-bucket/test_file.txt"
        response = test_client.post("/upload/", files={"file": upload_file})
        assert response.status_code == 200
        assert response.json() == {
            "message": "File uploaded successfully",
            "file_url": "http://s3-bucket/test_file.txt"
        }
    def test_validation_error(self, test_client: TestClient, mock_s3_service: Any,
                               mock_validate_file_type: Any, mock_validate_file_size: Any,
                               upload_file: UploadFile) -> None:
        """Test handling of validation errors during file upload.
        Purpose: Ensure that validation errors are correctly raised.
        Scenario: The file type validation fails.
        Expected outcome: A 400 response with an appropriate error message.
        """
        mock_validate_file_type.side_effect = ValueError("Invalid file type")
        response = test_client.post("/upload/", files={"file": upload_file})
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid file type"}
    def test_internal_server_error(self, test_client: TestClient, mock_s3_service: Any,
                                    mock_validate_file_type: Any, mock_validate_file_size: Any,
                                    upload_file: UploadFile) -> None:
        """Test handling of unexpected errors during file upload.
        Purpose: Verify that internal server errors are correctly raised.
        Scenario: The S3 service raises an unexpected exception during upload.
        Expected outcome: A 500 response indicating an internal server error.
        """
        mock_validate_file_type.return_value = None
        mock_validate_file_size.return_value = None
        mock_s3_service.return_value.upload_file_to_s3.side_effect = Exception("Upload failed")
        response = test_client.post("/upload/", files={"file": upload_file})
        assert response.status_code == 500
        assert response.json() == {"detail": "Internal Server Error"}
