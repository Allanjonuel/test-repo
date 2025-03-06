"""Unit tests for the FastAPI S3 Application main module."""
import pytest
from fastapi.testclient import TestClient
from src.fastapi_s3_app.app.main import app
@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """Fixture for creating a test client for the FastAPI application.
    Returns:
        TestClient: An instance of the FastAPI TestClient.
    """
    client = TestClient(app)
    yield client
class TestRootEndpoint:
    """Test suite for the root endpoint of the FastAPI S3 Application."""
    def test_root_endpoint(self, test_client: TestClient) -> None:
        """Test the root endpoint response.
        Purpose: Verify that the root endpoint returns the correct welcome message.
        Scenario: Send a GET request to the root endpoint ("/").
        Expected outcome: The response should contain a JSON object with the message "Welcome to the FastAPI S3 Application".
        Edge cases: None.
        """
        response = test_client.get("/")
        assert response.status_code == 200, "Expected status code 200"
        assert response.json() == {"message": "Welcome to the FastAPI S3 Application"}, "Unexpected response message"
    def test_root_endpoint_invalid_method(self, test_client: TestClient) -> None:
        """Test the root endpoint with an invalid HTTP method.
        Purpose: Verify that the root endpoint does not accept POST requests.
        Scenario: Send a POST request to the root endpoint ("/").
        Expected outcome: The response should have a status code of 405 (Method Not Allowed).
        Edge cases: Testing with different invalid methods.
        """
        response = test_client.post("/")
        assert response.status_code == 405, "Expected status code 405 for POST request"
    def test_root_endpoint_not_found(self, test_client: TestClient) -> None:
        """Test a non-existing endpoint to verify 404 response.
        Purpose: Ensure that a request to a nonexistent endpoint returns a 404 error.
        Scenario: Send a GET request to a random path ("/notfound").
        Expected outcome: The response should have a status code of 404.
        Edge cases: None.
        """
        response = test_client.get("/notfound")
        assert response.status_code == 404, "Expected status code 404 for non-existing endpoint"
"""End of test suite for the FastAPI S3 Application main module."""
