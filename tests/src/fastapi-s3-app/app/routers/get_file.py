"""
Test suite for the get_file module in the FastAPI S3 application.
This module tests the functionality of the get_file endpoint, ensuring
that the file retrieval from S3 behaves correctly under various scenarios,
including successful retrieval, file not found, and other internal errors.
"""
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.fastapi_s3_app.app.routers.get_file import router
@pytest.fixture(scope="module")
def client() -> TestClient:
    """Fixture for the FastAPI test client."""
    return TestClient(router)
@pytest.fixture
def mock_s3_service() -> MagicMock:
    """Fixture for mocking the S3Service."""
    with patch('src.fastapi_s3_app.app.routers.get_file.s3_service') as mock_service:
        yield mock_service
class TestGetFile:
    """Test class for the get_file endpoint."""
    def test_get_file_success(self, client: TestClient, mock_s3_service: MagicMock) -> None:
        """
        Test successful file retrieval from S3.
        Purpose: Verify that a file can be retrieved successfully.
        Scenario: A valid file name is provided, and the file exists in S3.
        Expected outcome: The response status code should be 200,
                          and the content should match the mocked file content.
        """
        mock_file_content = b"File content here"
        mock_s3_service.get_file_from_s3.return_value = mock_file_content
        response = client.get("/files/test_file.txt")
        assert response.status_code == 200, "Expected status code 200 for successful retrieval"
        assert response.content == mock_file_content, "Expected file content does not match"
    def test_get_file_not_found(self, client: TestClient, mock_s3_service: MagicMock) -> None:
        """
        Test file not found scenario from S3.
        Purpose: Verify the behavior when a file is not found.
        Scenario: A file name is provided that does not exist in S3.
        Expected outcome: The response status code should be 404, and the detail should indicate "File not found".
        """
        mock_s3_service.get_file_from_s3.side_effect = FileNotFoundError
        response = client.get("/files/non_existent_file.txt")
        assert response.status_code == 404, "Expected status code 404 for file not found"
        assert response.json() == {"detail": "File not found"}, "Expected error detail does not match"
    def test_get_file_internal_error(self, client: TestClient, mock_s3_service: MagicMock) -> None:
        """
        Test internal server error scenario from S3.
        Purpose: Verify the behavior when an unexpected error occurs during file retrieval.
        Scenario: A valid file name is provided, but an unexpected exception occurs.
        Expected outcome: The response status code should be 500, and the detail should indicate "Internal Server Error".
        """
        mock_s3_service.get_file_from_s3.side_effect = Exception("Unexpected error")
        response = client.get("/files/valid_file.txt")
        assert response.status_code == 500, "Expected status code 500 for internal server error"
        assert response.json() == {"detail": "Internal Server Error"}, "Expected error detail does not match"
