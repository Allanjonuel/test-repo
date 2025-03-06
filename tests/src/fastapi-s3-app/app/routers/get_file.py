"""Test suite for the get_file endpoint in the FastAPI S3 application.
This module includes tests for the functionality provided by the get_file
endpoint, ensuring it handles various scenarios including successful file
retrieval and error cases.
"""
import pytest
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from unittest.mock import patch, MagicMock
from src.fastapi_s3_app.app.routers.get_file import get_file
from app.services.s3_service import S3Service
class TestGetFile:
    """Test cases for the get_file endpoint."""
    @pytest.fixture(scope="function")
    def mock_s3_service(self) -> None:
        """Fixture to mock the S3Service for testing."""
        with patch("src.fastapi_s3_app.app.routers.get_file.s3_service") as mock_service:
            yield mock_service
    @pytest.mark.asyncio
    async def test_get_file_success(self, mock_s3_service: MagicMock) -> None:
        """Test successful file retrieval from S3.
        Purpose: Verify that the endpoint returns a StreamingResponse when
        the file is successfully retrieved.
        Scenario: The S3 service returns a valid file content.
        Expected outcome: The response is a StreamingResponse with the correct
        media type.
        Edge cases: None for this scenario.
        """
        mock_file_content = b"file content"
        mock_s3_service.get_file_from_s3.return_value = mock_file_content
        response = await get_file("testfile.txt")
        assert isinstance(response, StreamingResponse), "Response should be a StreamingResponse"
        assert response.media_type == "application/octet-stream", "Media type should be 'application/octet-stream'"
        assert await response.body() == mock_file_content, "Response body should match the file content"
    @pytest.mark.asyncio
    async def test_get_file_not_found(self, mock_s3_service: MagicMock) -> None:
        """Test retrieval of a non-existent file from S3.
        Purpose: Ensure that the endpoint raises a 404 HTTPException when
        the file is not found.
        Scenario: The S3 service raises FileNotFoundError.
        Expected outcome: An HTTPException with status code 404 is raised.
        Edge cases: None for this scenario.
        """
        mock_s3_service.get_file_from_s3.side_effect = FileNotFoundError
        with pytest.raises(HTTPException) as exc_info:
            await get_file("non_existent_file.txt")
        assert exc_info.value.status_code == 404, "Expected status code should be 404"
        assert exc_info.value.detail == "File not found", "Expected detail message should indicate file not found"
    @pytest.mark.asyncio
    async def test_get_file_internal_error(self, mock_s3_service: MagicMock) -> None:
        """Test internal server error handling.
        Purpose: Verify that the endpoint raises a 500 HTTPException for
        unexpected errors.
        Scenario: The S3 service raises a generic exception.
        Expected outcome: An HTTPException with status code 500 is raised.
        Edge cases: None for this scenario.
        """
        mock_s3_service.get_file_from_s3.side_effect = Exception("Unexpected error")
        with pytest.raises(HTTPException) as exc_info:
            await get_file("testfile.txt")
        assert exc_info.value.status_code == 500, "Expected status code should be 500"
        assert exc_info.value.detail == "Internal Server Error", "Expected detail message should indicate internal error"
    @pytest.mark.asyncio
    async def test_get_file_logging(self, mock_s3_service: MagicMock, caplog: pytest.LogCaptureFixture) -> None:
        """Test logging for file retrieval.
        Purpose: Verify logging behavior during file retrieval.
        Scenario: The S3 service returns a file successfully.
        Expected outcome: An info log message indicating successful retrieval.
        Edge cases: None for this scenario.
        """
        mock_file_content = b"file content"
        mock_s3_service.get_file_from_s3.return_value = mock_file_content
        await get_file("testfile.txt")
        assert "File testfile.txt retrieved successfully." in caplog.text, "Info log should indicate successful file retrieval"
    @pytest.mark.asyncio
    async def test_get_file_logging_error(self, mock_s3_service: MagicMock, caplog: pytest.LogCaptureFixture) -> None:
        """Test logging for file not found error.
        Purpose: Verify logging behavior during file retrieval failure.
        Scenario: The S3 service raises FileNotFoundError.
        Expected outcome: An error log message indicating file not found.
        Edge cases: None for this scenario.
        """
        mock_s3_service.get_file_from_s3.side_effect = FileNotFoundError
        with pytest.raises(HTTPException):
            await get_file("non_existent_file.txt")
        assert "File non_existent_file.txt not found." in caplog.text, "Error log should indicate file not found"
    @pytest.mark.asyncio
    async def test_get_file_logging_internal_error(self, mock_s3_service: MagicMock, caplog: pytest.LogCaptureFixture) -> None:
        """Test logging for internal server error.
        Purpose: Verify logging behavior for unexpected errors.
        Scenario: The S3 service raises a generic exception.
        Expected outcome: An error log message indicating a failure.
        Edge cases: None for this scenario.
        """
        mock_s3_service.get_file_from_s3.side_effect = Exception("Unexpected error")
        with pytest.raises(HTTPException):
            await get_file("testfile.txt")
        assert "Failed to retrieve file: Unexpected error" in caplog.text, "Error log should indicate failure to retrieve file"
