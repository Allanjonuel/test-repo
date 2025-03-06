import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from typing import Any, Dict
from src.fastapi_s3_app.app.main import app
@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """Fixture that provides a test client for the FastAPI application."""
    return TestClient(app)
class TestRootEndpoint:
    """Test suite for the root endpoint of the FastAPI application."""
    def test_root_endpoint(self, test_client: TestClient) -> None:
        """Test the root endpoint of the application.
        Purpose: Verify that the root endpoint returns the correct welcome message.
        Scenario: A GET request to the root endpoint ("/").
        Expected outcome: The response should return a JSON object with a welcome message.
        """
        response = test_client.get("/")
        assert response.status_code == 200, "Expected status code 200"
        assert response.json() == {"message": "Welcome to the FastAPI S3 Application"}, "Expected welcome message"
    def test_root_endpoint_not_found(self, test_client: TestClient) -> None:
        """Test the root endpoint with an invalid URL path.
        Purpose: Verify that an invalid path returns a 404 status code.
        Scenario: A GET request to an invalid endpoint (e.g., "/invalid").
        Expected outcome: The response should return a 404 status code.
        """
        response = test_client.get("/invalid")
        assert response.status_code == 404, "Expected status code 404"
    @patch("app.routers.upload")
    @patch("app.routers.list_files")
    @patch("app.routers.get_file")
    def test_included_routers(self, mock_upload, mock_list_files, mock_get_file, test_client: TestClient) -> None:
        """Test that the routers are included in the FastAPI app.
        Purpose: Ensure that the application includes the specified routers.
        Scenario: Verify that the mocked routers are included in the FastAPI app.
        Expected outcome: The mocked routers should be called without any errors.
        Edge cases: Verify the behavior when routers are incorrectly defined (mocked).
        """
        assert upload.router is not None, "Upload router should be included"
        assert list_files.router is not None, "List files router should be included"
        assert get_file.router is not None, "Get file router should be included"
        mock_upload.router.assert_called_once()
        mock_list_files.router.assert_called_once()
        mock_get_file.router.assert_called_once()
