"""
Test suite for the FastAPI S3 app's file listing router.
This module contains unit tests for the list_files function in the
src.fastapi-s3-app.app.routers.list_files module. It tests the successful
response when listing files as well as various error handling scenarios.
"""
import pytest
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from unittest.mock import AsyncMock, patch
from src.fastapi_s3_app.app.routers.list_files import router, list_files
@pytest.fixture(scope="module")
def mock_s3_service() -> AsyncMock:
    """Fixture to mock the S3Service for the duration of the module."""
    with patch("src.fastapi_s3_app.app.routers.list_files.s3_service") as mock:
        yield mock
class TestListFiles:
    """Test suite for the list_files function."""
    @pytest.mark.asyncio
    async def test_list_files_success(self, mock_s3_service: AsyncMock) -> None:
        """
        Purpose: Test successful retrieval of files from S3.
        Scenario: When the S3 service successfully lists files.
        Expected outcome: A JSONResponse with a status code of 200 and
        the list of files in the content.
        Edge cases: None.
        """
        mock_s3_service.list_files_in_s3.return_value = ["file1.txt", "file2.txt"]
        response: JSONResponse = await list_files()
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert response.content == {"files": ["file1.txt", "file2.txt"]}, (
            f"Expected content to be {{'files': ['file1.txt', 'file2.txt']}}, "
            f"but got {response.content}"
        )
    @pytest.mark.asyncio
    async def test_list_files_failure(self, mock_s3_service: AsyncMock) -> None:
        """
        Purpose: Test error handling when S3 service fails to list files.
        Scenario: When the S3 service raises an exception while listing files.
        Expected outcome: An HTTPException is raised with a status code of 500.
        Edge cases: None.
        """
        mock_s3_service.list_files_in_s3.side_effect = Exception("Service error")
        with pytest.raises(HTTPException) as exc_info:
            await list_files()
        assert exc_info.value.status_code == 500, (
            f"Expected status code 500, got {exc_info.value.status_code}"
        )
        assert exc_info.value.detail == "Internal Server Error", (
            f"Expected detail 'Internal Server Error', got '{exc_info.value.detail}'"
        )
    @pytest.mark.asyncio
    async def test_list_files_empty(self, mock_s3_service: AsyncMock) -> None:
        """
        Purpose: Test retrieval of files when no files are present in S3.
        Scenario: When the S3 service returns an empty list for files.
        Expected outcome: A JSONResponse with a status code of 200 and
        an empty list in the content.
        Edge cases: None.
        """
        mock_s3_service.list_files_in_s3.return_value = []
        response: JSONResponse = await list_files()
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert response.content == {"files": []}, (
            f"Expected content to be {{'files': []}}, but got {response.content}"
        )
    @pytest.mark.asyncio
    async def test_list_files_service_timeout(self, mock_s3_service: AsyncMock) -> None:
        """
        Purpose: Test error handling for S3 service timeout.
        Scenario: When the S3 service raises a timeout exception while listing files.
        Expected outcome: An HTTPException is raised with a status code of 500.
        Edge cases: None.
        """
        mock_s3_service.list_files_in_s3.side_effect = TimeoutError("Service timeout")
        with pytest.raises(HTTPException) as exc_info:
            await list_files()
        assert exc_info.value.status_code == 500, (
            f"Expected status code 500, got {exc_info.value.status_code}"
        )
        assert exc_info.value.detail == "Internal Server Error", (
            f"Expected detail 'Internal Server Error', got '{exc_info.value.detail}'"
        )
