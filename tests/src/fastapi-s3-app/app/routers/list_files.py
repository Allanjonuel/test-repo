"""Unit tests for the list_files router in the FastAPI S3 application.
This test suite ensures that the list_files endpoint behaves correctly,
including both successful responses and error handling scenarios.
"""
import pytest
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from unittest.mock import patch, AsyncMock
from src.fastapi_s3_app.app.routers.list_files import list_files
@pytest.fixture(scope="module")
def mock_s3_service():
    """Fixture that mocks the S3Service's list_files_in_s3 method."""
    with patch("src.fastapi_s3_app.app.routers.list_files.s3_service") as mock:
        yield mock
@pytest.mark.asyncio
class TestListFiles:
    """Test the list_files endpoint's functionality."""
    @pytest.mark.asyncio
    async def test_list_files_success(self, mock_s3_service: AsyncMock) -> None:
        """Test successful retrieval of files from S3.
        Purpose: Verify that the endpoint returns the expected list of files.
        Scenario: The S3Service successfully retrieves a list of files.
        Expected outcome: A JSONResponse with status 200 and the list of files.
        """
        mock_s3_service.list_files_in_s3.return_value = ["file1.txt", "file2.txt"]
        response: JSONResponse = await list_files()
        assert response.status_code == 200, "Expected response status code to be 200"
        assert response.content == {"files": ["file1.txt", "file2.txt"]}, "Expected file list to match"
    @pytest.mark.asyncio
    async def test_list_files_service_failure(self, mock_s3_service: AsyncMock) -> None:
        """Test handling of exceptions when listing files.
        Purpose: Ensure that an internal server error is raised when the service fails.
        Scenario: The S3Service raises an exception during file retrieval.
        Expected outcome: An HTTPException with status 500.
        """
        mock_s3_service.list_files_in_s3.side_effect = Exception("Service error")
        with pytest.raises(HTTPException) as exc_info:
            await list_files()
        assert exc_info.value.status_code == 500, "Expected HTTP status code to be 500"
        assert exc_info.value.detail == "Internal Server Error", "Expected error detail message mismatch"
    @pytest.mark.asyncio
    async def test_list_files_empty(self, mock_s3_service: AsyncMock) -> None:
        """Test retrieval of an empty file list.
        Purpose: Verify the behavior when no files are available in S3.
        Scenario: The S3Service returns an empty list.
        Expected outcome: A JSONResponse with status 200 and an empty list.
        """
        mock_s3_service.list_files_in_s3.return_value = []
        response: JSONResponse = await list_files()
        assert response.status_code == 200, "Expected response status code to be 200"
        assert response.content == {"files": []}, "Expected file list to be empty"
    @pytest.mark.asyncio
    async def test_list_files_partial_failure(self, mock_s3_service: AsyncMock) -> None:
        """Test behavior when some files cannot be retrieved.
        Purpose: Ensure appropriate handling when a partial failure occurs.
        Scenario: The S3Service raises an exception for some files but returns others.
        Expected outcome: This scenario is not directly tested since logic for partial failures is not implemented yet.
        """
        pass
