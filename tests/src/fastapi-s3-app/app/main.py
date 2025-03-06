"""Unit tests for the FastAPI S3 Application main module.
This test suite covers the root endpoint of the FastAPI application, ensuring that it
responds correctly and handles various scenarios.
"""
import pytest
from fastapi.testclient import TestClient
from src.fastapi_s3_app.app.main import app
@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """Fixture to provide a test client for the FastAPI application.
    This fixture creates an instance of TestClient that can be used to make requests
    to the FastAPI app during the test lifecycle.
    """
    client = TestClient(app)
    yield client
class TestRootEndpoint:
    """Test suite for the root endpoint of the FastAPI application."""
    def test_root_endpoint_returns_welcome_message(self, test_client: TestClient) -> None:
        """Test that the root endpoint returns the welcome message.
        Purpose: Verify the response from the root endpoint.
        Scenario: Sending a GET request to the root endpoint.
        Expected outcome: The response should contain the welcome message.
        Edge cases: None for this simple endpoint.
        """
        response = test_client.get("/")
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert response.json() == {"message": "Welcome to the FastAPI S3 Application"}, \
            f"Expected response JSON to be {{'message': 'Welcome to the FastAPI S3 Application'}}, " \
            f"got {response.json()}"
    def test_root_endpoint_invalid_method(self, test_client: TestClient) -> None:
        """Test that the root endpoint does not accept non-GET methods.
        Purpose: Ensure that the root endpoint rejects non-GET requests.
        Scenario: Sending a POST request to the root endpoint.
        Expected outcome: The response should return a 405 Method Not Allowed status.
        Edge cases: Testing other HTTP methods.
        """
        response = test_client.post("/")
        assert response.status_code == 405, f"Expected status code 405, got {response.status_code}"
    def test_root_endpoint_invalid_endpoint(self, test_client: TestClient) -> None:
        """Test that accessing an invalid endpoint returns a 404 error.
        Purpose: Verify the behavior of the application when accessing a non-existent endpoint.
        Scenario: Sending a GET request to a random invalid endpoint.
        Expected outcome: The response should return a 404 Not Found status.
        Edge cases: Accessing various random endpoints.
        """
        response = test_client.get("/invalid-endpoint")
        assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"
