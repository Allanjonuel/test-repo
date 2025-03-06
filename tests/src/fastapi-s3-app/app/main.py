"""
Test suite for the FastAPI S3 Application main module.
This test module contains unit tests for the FastAPI application defined in
the src.fastapi-s3-app.app.main module. It focuses on verifying the root
endpoint and ensuring that the application setup is correct.
"""
import pytest
from fastapi.testclient import TestClient
from src.fastapi-s3-app.app.main import app
@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """Fixture to create a test client for the FastAPI application."""
    with TestClient(app) as client:
        yield client
class TestRootEndpoint:
    """Test suite for the root endpoint of the FastAPI application."""
    def test_root_endpoint(self, test_client: TestClient) -> None:
        """
        Purpose: Verify the root endpoint returns the expected welcome message.
        Scenario: Accessing the root endpoint ("/") of the application.
        Expected outcome: The response should contain a JSON object with the
                          message "Welcome to the FastAPI S3 Application".
        Edge cases: None for this specific endpoint.
        """
        response = test_client.get("/")
        assert response.status_code == 200, "Expected status code 200"
        assert response.json() == {"message": "Welcome to the FastAPI S3 Application"}, \
            "Expected welcome message not found in response"
    def test_root_endpoint_not_found(self, test_client: TestClient) -> None:
        """
        Purpose: Ensure that accessing an invalid endpoint returns a 404 status.
        Scenario: Accessing an invalid path ("/invalid").
        Expected outcome: The response status should be 404.
        Edge cases: Testing a path that does not exist.
        """
        response = test_client.get("/invalid")
        assert response.status_code == 404, "Expected status code 404 for invalid endpoint"
