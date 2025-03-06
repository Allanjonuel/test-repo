"""
Test suite for the get_file endpoint in the FastAPI S3 application.
This module tests the functionality of the get_file API endpoint, ensuring that it correctly retrieves files from S3, handles errors, and returns appropriate responses.
"""
import pytest
from typing import Any
from fastapi import HTTPException
from fastapi.testclient import TestClient
from src.fastapi_s3_app.app.routers.get_file import router
from unittest.mock import MagicMock, patch
@pytest.fixture(scope="module")
def client() -> TestClient:
    """
    Fixture to create a TestClient for the FastAPI app.
    Returns:
        TestClient: A client for testing FastAPI endpoints.
    """
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)
@pytest.fixture(scope="function")
def mock_s3_service() -> Any:
    """
    Fixture to mock the S3Service for testing.
    Returns:
        MagicMock: A mock instance of the S3Service.
    """
    with patch("src.fastapi_s3_app.app.routers.get_file.s3_service") as mock_service:
        yield mock_service
class TestGetFile:
    """
    Test cases for the get_file endpoint.
    """
    def test_get_file_success(self, client: TestClient, mock_s3_service: MagicMock) -> None:
        """
        Purpose: Test successful file retrieval from S3.
        Scenario: A valid file name is provided, and the file exists.
        Expected outcome: The response should return status code 200 and a StreamingResponse.
        """
        file_name = "test_file.txt"
        mock_file_content = b"Sample file content"
        mock_s3_service.get_file_from_s3.return_value = mock_file_content
        response = client.get(f"/files/{file_name}")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert response.headers["content-type"] == "application/octet-stream"
        assert response.content == mock_file_content
    def test_get_file_not_found(self, client: TestClient, mock_s3_service: MagicMock) -> None:
        """
        Purpose: Test file retrieval failure when the file does not exist.
        Scenario: A valid file name is provided, but the file is not found in S3.
        Expected outcome: The response should return status code 404 and an error message.
        """
        file_name = "non_existent_file.txt"
        mock_s3_service.get_file_from_s3.side_effect = FileNotFoundError
        response = client.get(f"/files/{file_name}")
        assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"
        assert response.json() == {"detail": "File not found"}
    def test_get_file_internal_error(self, client: TestClient, mock_s3_service: MagicMock) -> None:
        """
        Purpose: Test internal server error on S3 service failure.
        Scenario: A valid file name is provided, but an unexpected error occurs.
        Expected outcome: The response should return status code 500 and an error message.
        """
        file_name = "test_file.txt"
        mock_s3_service.get_file_from_s3.side_effect = Exception("Unexpected error")
        response = client.get(f"/files/{file_name}")
        assert response.status_code == 500, f"Expected status code 500, got {response.status_code}"
        assert response.json() == {"detail": "Internal Server Error"}
