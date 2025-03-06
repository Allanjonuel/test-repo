"""
Test suite for the get_file router in the FastAPI application.
This module tests the behavior of the get_file endpoint for file retrieval from S3.
"""
import pytest
from typing import Any, Generator
from fastapi import HTTPException
from fastapi.testclient import TestClient
from src.fastapi-s3-app.app.routers.get_file import router
from unittest.mock import patch, MagicMock
@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """
    Fixture for creating a test client for the FastAPI app.
    Returns:
        TestClient: A test client to interact with the FastAPI application.
    """
    app = FastAPI()
    app.include_router(router)
    yield TestClient(app)
@pytest.fixture
def mock_s3_service() -> Any:
    """
    Fixture for mocking the S3Service to avoid actual S3 calls.
    Returns:
        MagicMock: A mocked instance of S3Service.
    """
    with patch("src.fastapi-s3-app.app.routers.get_file.s3_service") as mock:
        yield mock
class TestGetFile:
    """
    Test class for the get_file endpoint in the FastAPI application.
    This class covers various scenarios including successful retrieval and error handling.
    """
    def test_get_file_success(self, client: TestClient, mock_s3_service: Any) -> None:
        """
        Test the successful retrieval of a file from S3.
        Purpose: Verify that the endpoint returns a StreamingResponse on successful file retrieval.
        Scenario: Requesting an existing file should return its content.
        Expected outcome: The response should have status code 200 and the correct media type.
        """
        file_name = "test_file.txt"
        mock_content = b"File content"
        mock_s3_service.get_file_from_s3.return_value = mock_content
        response = client.get(f"/files/{file_name}")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert response.headers["content-type"] == "application/octet-stream"
        assert response.content == mock_content
    def test_get_file_not_found(self, client: TestClient, mock_s3_service: Any) -> None:
        """
        Test the behavior when the requested file is not found.
        Purpose: Verify that the endpoint raises a 404 error when the file does not exist.
        Scenario: Requesting a non-existing file should raise an HTTPException.
        Expected outcome: The response should have status code 404 and an appropriate error message.
        """
        file_name = "non_existent_file.txt"
        mock_s3_service.get_file_from_s3.side_effect = FileNotFoundError
        response = client.get(f"/files/{file_name}")
        assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"
        assert response.json() == {"detail": "File not found"}
    def test_get_file_internal_server_error(self, client: TestClient, mock_s3_service: Any) -> None:
        """
        Test the behavior when an unexpected error occurs.
        Purpose: Verify that the endpoint raises a 500 error for unexpected exceptions.
        Scenario: Simulating an unexpected error during file retrieval.
        Expected outcome: The response should have status code 500 and a generic error message.
        """
        file_name = "test_file.txt"
        mock_s3_service.get_file_from_s3.side_effect = Exception("Unexpected error")
        response = client.get(f"/files/{file_name}")
        assert response.status_code == 500, f"Expected status code 500, got {response.status_code}"
        assert response.json() == {"detail": "Internal Server Error"}
