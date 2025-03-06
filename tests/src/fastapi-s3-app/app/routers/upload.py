import pytest
from typing import Any
from fastapi import UploadFile
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.fastapi_s3_app.app.routers.upload import router
@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """Fixture to create a test client for the FastAPI application."""
    return TestClient(router)
@pytest.fixture
def mock_s3_service() -> Any:
    """Fixture to mock the S3Service for testing."""
    with patch('src.fastapi_s3_app.app.routers.upload.S3Service') as mock:
        yield mock
@pytest.fixture
def valid_file() -> UploadFile:
    """Fixture to create a valid UploadFile object for testing."""
    file_mock = MagicMock(spec=UploadFile)
    file_mock.filename = "test_file.txt"
    file_mock.content_type = "text/plain"
    file_mock.file = MagicMock()
    return file_mock
@pytest.fixture
def invalid_file() -> UploadFile:
    """Fixture to create an invalid UploadFile object for testing."""
    file_mock = MagicMock(spec=UploadFile)
    file_mock.filename = "invalid_file.exe"
    file_mock.content_type = "application/octet-stream"
    file_mock.file = MagicMock()
    return file_mock
class TestUploadFile:
    """Test suite for the upload_file function."""
    @pytest.mark.asyncio
    async def test_upload_file_success(self, test_client: TestClient, mock_s3_service: Any, valid_file: UploadFile) -> None:
        """
        Purpose: Test successful file upload to S3.
        Scenario: A valid file is uploaded.
        Expected outcome: The function returns a success message with file URL.
        """
        mock_s3_service.return_value.upload_file_to_s3.return_value = "https://example.com/test_file.txt"
        response = test_client.post("/upload/", files={"file": valid_file})
        assert response.status_code == 200
        assert response.json() == {"message": "File uploaded successfully", "file_url": "https://example.com/test_file.txt"}
    @pytest.mark.asyncio
    async def test_upload_file_validation_error(self, test_client: TestClient, mock_s3_service: Any, invalid_file: UploadFile) -> None:
        """
        Purpose: Test file upload with validation error.
        Scenario: An invalid file type is uploaded.
        Expected outcome: The function raises a 400 HTTPException with a validation error message.
        """
        mock_s3_service.return_value.upload_file_to_s3.side_effect = ValueError("Invalid file type")
        response = test_client.post("/upload/", files={"file": invalid_file})
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid file type"}
    @pytest.mark.asyncio
    async def test_upload_file_internal_server_error(self, test_client: TestClient, mock_s3_service: Any, valid_file: UploadFile) -> None:
        """
        Purpose: Test file upload that triggers an internal server error.
        Scenario: An unexpected error occurs during file upload.
        Expected outcome: The function raises a 500 HTTPException.
        """
        mock_s3_service.return_value.upload_file_to_s3.side_effect = Exception("Upload failed")
        response = test_client.post("/upload/", files={"file": valid_file})
        assert response.status_code == 500
        assert response.json() == {"detail": "Internal Server Error"}
    @pytest.mark.asyncio
    async def test_upload_file_missing_file(self, test_client: TestClient) -> None:
        """
        Purpose: Test file upload with missing file parameter.
        Scenario: No file is provided in the request.
        Expected outcome: The function raises a 422 HTTPException due to validation error.
        """
        response = test_client.post("/upload/")
        assert response.status_code == 422  # Unprocessable Entity for missing file
    @pytest.mark.asyncio
    async def test_upload_file_empty_file(self, test_client: TestClient, mock_s3_service: Any) -> None:
        """
        Purpose: Test file upload with an empty file.
        Scenario: An empty file is uploaded.
        Expected outcome: The function raises a validation error indicating the file is empty.
        """
        empty_file_mock = MagicMock(spec=UploadFile)
        empty_file_mock.filename = "empty_file.txt"
        empty_file_mock.file.read.return_value = b''  # Simulate empty file
        mock_s3_service.return_value.upload_file_to_s3.side_effect = ValueError("File is empty")
        response = test_client.post("/upload/", files={"file": empty_file_mock})
        assert response.status_code == 400
        assert response.json() == {"detail": "File is empty"}
