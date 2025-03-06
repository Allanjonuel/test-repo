"""
Test suite for the upload functionality of the FastAPI application.
This module contains unit tests for the upload_file endpoint in the upload router,
ensuring correct behavior with various file uploads and error handling scenarios.
"""
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from typing import Any
from unittest.mock import patch, MagicMock
from src.fastapi_s3_app.app.routers.upload import router
@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """Creates a test client for the FastAPI application."""
    client = TestClient(router)
    return client
@pytest.fixture
def mock_s3_service() -> Any:
    """Mocks the S3Service to simulate file upload behavior."""
    with patch("src.fastapi_s3_app.app.routers.upload.S3Service") as mock_service:
        yield mock_service
@pytest.fixture
def valid_file() -> UploadFile:
    """Creates a valid UploadFile object for testing."""
    return MagicMock(spec=UploadFile, name='valid_file', filename='test_file.txt', content_type='text/plain')
@pytest.fixture
def invalid_file_type() -> UploadFile:
    """Creates an invalid UploadFile object for testing."""
    return MagicMock(spec=UploadFile, name='invalid_file', filename='test_file.exe', content_type='application/x-msdownload')
@pytest.fixture
def invalid_file_size() -> UploadFile:
    """Creates a valid UploadFile object with an invalid size for testing."""
    file_mock = MagicMock(spec=UploadFile, name='large_file', filename='large_file.txt', content_type='text/plain')
    file_mock.file = MagicMock()  # Mock the file attribute
    file_mock.file.seek.return_value = None  # Mock seek to avoid errors
    file_mock.file.read.return_value = b"x" * (10 * 1024 * 1024 + 1)  # Mock file size over 10 MB
    return file_mock
class TestUploadFile:
    """Test cases for the upload_file endpoint."""
    @pytest.mark.asyncio
    async def test_upload_file_success(self, test_client: TestClient, mock_s3_service: Any, valid_file: UploadFile) -> None:
        """
        Test the successful upload of a valid file.
        Scenario: A valid file is uploaded to the S3 bucket.
        Expected outcome: The response should indicate success with the file URL.
        """
        mock_s3_service.return_value.upload_file_to_s3.return_value = "http://s3.amazonaws.com/test_file.txt"
        response = test_client.post("/upload/", files={"file": valid_file})
        assert response.status_code == 200
        assert response.json() == {
            "message": "File uploaded successfully",
            "file_url": "http://s3.amazonaws.com/test_file.txt"
        }
    @pytest.mark.asyncio
    async def test_upload_file_invalid_type(self, test_client: TestClient, mock_s3_service: Any, invalid_file_type: UploadFile) -> None:
        """
        Test the upload of a file with an invalid type.
        Scenario: An invalid file type is uploaded.
        Expected outcome: The response should indicate a validation error.
        """
        mock_s3_service.return_value.upload_file_to_s3.side_effect = ValueError("Invalid file type")
        response = test_client.post("/upload/", files={"file": invalid_file_type})
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid file type"}
    @pytest.mark.asyncio
    async def test_upload_file_invalid_size(self, test_client: TestClient, mock_s3_service: Any, invalid_file_size: UploadFile) -> None:
        """
        Test the upload of a file that exceeds the size limit.
        Scenario: An oversized file is uploaded.
        Expected outcome: The response should indicate a validation error.
        """
        mock_s3_service.return_value.upload_file_to_s3.side_effect = ValueError("File size exceeds limit")
        response = test_client.post("/upload/", files={"file": invalid_file_size})
        assert response.status_code == 400
        assert response.json() == {"detail": "File size exceeds limit"}
    @pytest.mark.asyncio
    async def test_upload_file_internal_error(self, test_client: TestClient, mock_s3_service: Any, valid_file: UploadFile) -> None:
        """
        Test handling of an internal server error during file upload.
        Scenario: An unexpected error occurs during file upload.
        Expected outcome: The response should indicate an internal server error.
        """
        mock_s3_service.return_value.upload_file_to_s3.side_effect = Exception("Internal error occurred")
        response = test_client.post("/upload/", files={"file": valid_file})
        assert response.status_code == 500
        assert response.json() == {"detail": "Internal Server Error"}
