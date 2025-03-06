"""Unit tests for the list_files module in the FastAPI S3 application.
This test suite verifies the behavior of the list_files endpoint, ensuring that it correctly lists files from S3 and handles errors appropriately.
"""
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.fastapi_s3_app.app.routers.list_files import router
@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """Create a test client for the FastAPI application.
    Returns:
        TestClient: An instance of the FastAPI test client.
    """
    return TestClient(router)
@pytest.fixture
def mock_s3_service() -> MagicMock:
    """Mock the S3Service to simulate file listing.
    Returns:
        MagicMock: A mocked instance of S3Service.
    """
    with patch("src.fastapi_s3_app.app.routers.list_files.s3_service") as mock_service:
        yield mock_service
class TestListFiles:
    """Test cases for the list_files endpoint."""
    def test_list_files_success(self, test_client: TestClient, mock_s3_service: MagicMock) -> None:
        """Test successful retrieval of files from S3.
        Purpose: Verify that the endpoint returns a list of files successfully.
        Scenario: The S3 service lists files without errors.
        Expected outcome: The response contains a status code 200 and a list of files.
        Edge cases: None for this scenario.
        """
        mock_s3_service.list_files_in_s3.return_value = ["file1.txt", "file2.txt"]
        response = test_client.get("/files/")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert response.json() == {"files": ["file1.txt", "file2.txt"]}, f"Unexpected response content: {response.json()}"
    def test_list_files_failure(self, test_client: TestClient, mock_s3_service: MagicMock) -> None:
        """Test failure in retrieving files from S3.
        Purpose: Verify that the endpoint handles errors when the S3 service fails.
        Scenario: The S3 service raises an exception.
        Expected outcome: The response contains a status code 500 and an error message.
        Edge cases: None for this scenario.
        """
        mock_s3_service.list_files_in_s3.side_effect = Exception("S3 service error")
        response = test_client.get("/files/")
        assert response.status_code == 500, f"Expected status code 500, got {response.status_code}"
        assert response.json() == {"detail": "Internal Server Error"}, f"Unexpected response content: {response.json()}"
    def test_list_files_empty_response(self, test_client: TestClient, mock_s3_service: MagicMock) -> None:
        """Test retrieval of files when no files are present in S3.
        Purpose: Verify that the endpoint returns an empty list when there are no files.
        Scenario: The S3 service returns an empty list.
        Expected outcome: The response contains a status code 200 and an empty list of files.
        Edge cases: None for this scenario.
        """
        mock_s3_service.list_files_in_s3.return_value = []
        response = test_client.get("/files/")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert response.json() == {"files": []}, f"Unexpected response content: {response.json()}"
    def test_list_files_service_unavailable(self, test_client: TestClient, mock_s3_service: MagicMock) -> None:
        """Test failure when S3 service is unavailable.
        Purpose: Verify that the endpoint returns a 500 error when the service is unavailable.
        Scenario: The S3 service is unreachable.
        Expected outcome: The response contains a status code 500 and an error message.
        Edge cases: None for this scenario.
        """
        mock_s3_service.list_files_in_s3.side_effect = ConnectionError("Service unavailable")
        response = test_client.get("/files/")
        assert response.status_code == 500, f"Expected status code 500, got {response.status_code}"
        assert response.json() == {"detail": "Internal Server Error"}, f"Unexpected response content: {response.json()}"
    def test_list_files_timeout(self, test_client: TestClient, mock_s3_service: MagicMock) -> None:
        """Test handling of timeout exception while listing files.
        Purpose: Verify that the endpoint handles timeout exceptions.
        Scenario: The S3 service raises a timeout exception.
        Expected outcome: The response contains a status code 500 and an error message.
        Edge cases: None for this scenario.
        """
        mock_s3_service.list_files_in_s3.side_effect = TimeoutError("Timeout occurred")
        response = test_client.get("/files/")
        assert response.status_code == 500, f"Expected status code 500, got {response.status_code}"
        assert response.json() == {"detail": "Internal Server Error"}, f"Unexpected response content: {response.json()}"
    def test_list_files_logging(self, mock_s3_service: MagicMock, caplog: pytest.LogCaptureFixture) -> None:
        """Test logging during the file listing process.
        Purpose: Verify that appropriate logs are created during file listing.
        Scenario: The S3 service successfully lists files.
        Expected outcome: Logs indicate successful file listing.
        Edge cases: None for this scenario.
        """
        mock_s3_service.list_files_in_s3.return_value = ["file1.txt"]
        with caplog.at_level(logging.INFO):
            test_client().get("/files/")
        assert "Files listed successfully." in caplog.text, "Expected log message not found."
    def test_list_files_logging_failure(self, mock_s3_service: MagicMock, caplog: pytest.LogCaptureFixture) -> None:
        """Test logging during a failure to list files.
        Purpose: Verify that error logs are created when the S3 service fails.
        Scenario: The S3 service raises an exception.
        Expected outcome: Logs indicate that file listing failed.
        Edge cases: None for this scenario.
        """
        mock_s3_service.list_files_in_s3.side_effect = Exception("Error")
        with caplog.at_level(logging.ERROR):
            test_client().get("/files/")
        assert "Failed to list files: Error" in caplog.text, "Expected error log message not found."
