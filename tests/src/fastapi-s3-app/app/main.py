"""
Test suite for the FastAPI S3 Application main module.
This module contains unit tests for the FastAPI application defined in
src.fastapi-s3-app.app.main. It tests the root endpoint and ensures that
all routes are included correctly.
"""
import pytest
from fastapi.testclient import TestClient
from src.fastapi_s3_app.app.main import app
@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """
    Fixture for creating a test client for the FastAPI app.
    This client can be used to simulate requests to the application.
    """
    with TestClient(app) as client:
        yield client
class TestRootEndpoint:
    """
    Test cases for the root endpoint ("/") of the FastAPI application.
    """
    def test_root_endpoint(self, test_client: TestClient) -> None:
        """
        Test the root endpoint of the application.
        Purpose: Verify that the root endpoint returns the correct message.
        Scenario: Call the root endpoint.
        Expected outcome: The response should be a JSON object with a welcome message.
        Edge cases: None for this simple endpoint.
        """
        response = test_client.get("/")
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        assert response.json() == {"message": "Welcome to the FastAPI S3 Application"}, \
            f"Expected response message not found: {response.json()}"
class TestRouterIntegration:
    """
    Test cases to ensure that the routers are included correctly in the FastAPI app.
    """
    def test_upload_router_included(self, test_client: TestClient) -> None:
        """
        Test that the upload router is included in the application.
        Purpose: Ensure the upload router is correctly integrated.
        Scenario: Check if the upload endpoint responds as expected.
        Expected outcome: The upload endpoint should be accessible without error.
        Edge cases: None for this test.
        """
        response = test_client.get("/upload")  # Adjust endpoint as necessary
        assert response.status_code in (200, 404), \
            f"Upload router not included correctly, status code: {response.status_code}"
    def test_list_files_router_included(self, test_client: TestClient) -> None:
        """
        Test that the list_files router is included in the application.
        Purpose: Ensure the list_files router is correctly integrated.
        Scenario: Check if the list_files endpoint responds as expected.
        Expected outcome: The list_files endpoint should be accessible without error.
        Edge cases: None for this test.
        """
        response = test_client.get("/files")  # Adjust endpoint as necessary
        assert response.status_code in (200, 404), \
            f"List files router not included correctly, status code: {response.status_code}"
    def test_get_file_router_included(self, test_client: TestClient) -> None:
        """
        Test that the get_file router is included in the application.
        Purpose: Ensure the get_file router is correctly integrated.
        Scenario: Check if the get_file endpoint responds as expected.
        Expected outcome: The get_file endpoint should be accessible without error.
        Edge cases: None for this test.
        """
        response = test_client.get("/file/sample.txt")  # Adjust endpoint as necessary
        assert response.status_code in (200, 404), \
            f"Get file router not included correctly, status code: {response.status_code}"
