"""
Test suite for the get_file router in the FastAPI application.
This module tests the functionality of the get_file endpoint,
ensuring correct responses for valid and invalid file requests.
"""
from typing import Any, Generator
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.fastapi_s3_app.app.routers.get_file import router
@pytest.fixture(scope="module")
def test_client() -> Generator[TestClient, None, None]:
    """Fixture to create a test client for the FastAPI application."""
    app = FastAPI()
    app.include_router(router)
    with TestClient(app) as client:
        yield client
@pytest.fixture
def mock_s3_service() -> Generator[None, None, None]:
    """Fixture to mock S3Service for testing."""
    with patch('src.fastapi_s3_app.app.routers.get_file.s3_service') as mock_service:
        yield mock_service
class TestGetFile:
    """Test cases for the get_file endpoint."""
    @pytest.fixture
    def valid_file_content(self) -> Any:
        """Fixture providing valid file content for testing."""
        return b"File content goes here."
    @pytest.mark.asyncio
    async def test_get_file_success(self, test_client: TestClient, mock_s3_service: MagicMock, valid_file_content: Any) -> None:
        """
        Purpose: Test successful retrieval of a file from S3.
        Scenario: When a valid file name is provided.
        Expected outcome: The endpoint returns a StreamingResponse with file content.
        """
        mock_s3_service.get_file_from_s3.return_value = valid_file_content
        response = test_client.get("/files/testfile.txt")
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        assert response.content == valid_file_content, "The file content returned does not match the expected content."
    @pytest.mark.asyncio
    async def test_get_file_not_found(self, test_client: TestClient, mock_s3_service: MagicMock) -> None:
        """
        Purpose: Test retrieval of a file that does not exist in S3.
        Scenario: When a non-existent file name is provided.
        Expected outcome: The endpoint raises a 404 HTTPException.
        """
        mock_s3_service.get_file_from_s3.side_effect = FileNotFoundError("File not found")
        response = test_client.get("/files/nonexistentfile.txt")
        assert response.status_code == 404, f"Expected status code 404 but got {response.status_code}"
        assert response.json() == {"detail": "File not found"}, "Error message does not match expected."
    @pytest.mark.asyncio
    async def test_get_file_internal_server_error(self, test_client: TestClient, mock_s3_service: MagicMock) -> None:
        """
        Purpose: Test internal server error handling for the get_file endpoint.
        Scenario: When an unexpected error occurs during file retrieval.
        Expected outcome: The endpoint raises a 500 HTTPException.
        """
        mock_s3_service.get_file_from_s3.side_effect = Exception("Unexpected error")
        response = test_client.get("/files/somefile.txt")
        assert response.status_code == 500, f"Expected status code 500 but got {response.status_code}"
        assert response.json() == {"detail": "Internal Server Error"}, "Error message does not match expected."
    @pytest.mark.asyncio
    async def test_get_file_empty_filename(self, test_client: TestClient, mock_s3_service: MagicMock) -> None:
        """
        Purpose: Test behavior when an empty file name is provided.
        Scenario: When an empty string is passed as the file name.
        Expected outcome: The endpoint raises a 404 HTTPException.
        Edge cases: Tests handling of empty input.
        """
        response = test_client.get("/files/")
        assert response.status_code == 404, f"Expected status code 404 but got {response.status_code}"
        assert response.json() == {"detail": "File not found"}, "Error message does not match expected."
