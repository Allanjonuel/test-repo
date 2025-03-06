"""Unit tests for the list_files router in the FastAPI S3 application.
This test suite verifies the functionality of the list_files endpoint, ensuring that it correctly lists files and handles errors appropriately.
"""
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from src.fastapi_s3_app.app.routers.list_files import router
from unittest.mock import patch, MagicMock
@pytest.fixture(scope="module")
def client() -> TestClient:
    """Create a FastAPI test client for making requests to the router.
    Returns:
        TestClient: A test client for the FastAPI application.
    """
    return TestClient(router)
@pytest.fixture
def mock_s3_service() -> MagicMock:
    """Create a mock instance of S3Service for testing.
    Returns:
        MagicMock: A mock instance of the S3Service.
    """
    with patch("src.fastapi_s3_app.app.routers.list_files.s3_service") as mock_service:
        yield mock_service
class TestListFiles:
    """Test cases for the list_files endpoint."""
    def test_list_files_success(self, client: TestClient, mock_s3_service: MagicMock) -> None:
        """Test successful retrieval of files from S3.
        Purpose: Verify that the endpoint returns a list of files when S3 service is successful.
        Scenario: S3 service returns a list of file names.
        Expected outcome: The response status code is 200 and contains the list of files.
        Edge cases: None.
        """
        mock_s3_service.list_files_in_s3.return_value = ["file1.txt", "file2.txt"]
        response = client.get("/files/")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert response.json() == {"files": ["file1.txt", "file2.txt"]}, f"Unexpected response content: {response.json()}"
    def test_list_files_service_failure(self, client: TestClient, mock_s3_service: MagicMock) -> None:
        """Test failure when S3 service raises an exception.
        Purpose: Verify that the endpoint raises an HTTPException when S3 service fails.
        Scenario: S3 service raises an exception when listing files.
        Expected outcome: The response status code is 500 with an appropriate error message.
        Edge cases: None.
        """
        mock_s3_service.list_files_in_s3.side_effect = Exception("Service unavailable")
        response = client.get("/files/")
        assert response.status_code == 500, f"Expected status code 500, got {response.status_code}"
        assert response.json() == {"detail": "Internal Server Error"}, f"Unexpected response content: {response.json()}"
    def test_list_files_empty_response(self, client: TestClient, mock_s3_service: MagicMock) -> None:
        """Test behavior when S3 service returns an empty list.
        Purpose: Verify that the endpoint can handle an empty list of files.
        Scenario: S3 service returns an empty list.
        Expected outcome: The response status code is 200 and the files list is empty.
        Edge cases: None.
        """
        mock_s3_service.list_files_in_s3.return_value = []
        response = client.get("/files/")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert response.json() == {"files": []}, f"Unexpected response content: {response.json()}"
    def test_list_files_service_error_logging(self, client: TestClient, mock_s3_service: MagicMock) -> None:
        """Test logging when S3 service raises an exception.
        Purpose: Verify that an error is logged when S3 service fails.
        Scenario: S3 service raises an exception when listing files.
        Expected outcome: The logging should capture the error message.
        Edge cases: None.
        """
        mock_s3_service.list_files_in_s3.side_effect = Exception("Service unavailable")
        with patch("src.fastapi_s3_app.app.routers.list_files.logger") as mock_logger:
            response = client.get("/files/")
            mock_logger.error.assert_called_once_with("Failed to list files: Service unavailable")
        assert response.status_code == 500, f"Expected status code 500, got {response.status_code}"
        assert response.json() == {"detail": "Internal Server Error"}, f"Unexpected response content: {response.json()}"
