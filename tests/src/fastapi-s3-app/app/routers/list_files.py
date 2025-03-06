"""
Test suite for the list_files router in the FastAPI S3 application.
This module contains unit tests for the list_files endpoint, ensuring that it behaves correctly under
various scenarios, including successful file retrieval and error handling.
"""
import pytest
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from unittest.mock import patch, MagicMock
from typing import Any, Dict
from src.fastapi_s3_app.app.routers.list_files import router, list_files
@pytest.fixture(scope="module")
def mock_s3_service() -> MagicMock:
    """
    Fixture that mocks the S3Service to isolate tests from external dependencies.
    Returns:
        MagicMock: A mock instance of S3Service.
    """
    mock_service = MagicMock()
    with patch("src.fastapi_s3_app.app.routers.list_files.s3_service", mock_service):
        yield mock_service
@pytest.mark.asyncio
class TestListFiles:
    """
    Test cases for the list_files endpoint of the FastAPI application.
    """
    async def test_list_files_success(self, mock_s3_service: MagicMock) -> None:
        """
        Purpose: Test successful retrieval of files from S3.
        Scenario: When the S3 service returns a list of files.
        Expected outcome: A JSON response with status code 200 and a list of files.
        Edge cases: None.
        """
        expected_files = ["file1.txt", "file2.txt"]
        mock_s3_service.list_files_in_s3.return_value = expected_files
        response: JSONResponse = await list_files()
        assert response.status_code == 200, "Expected status code 200 for successful file retrieval."
        assert response.content == {"files": expected_files}, "Expected response content to match the list of files."
    async def test_list_files_failure(self, mock_s3_service: MagicMock) -> None:
        """
        Purpose: Test handling of exceptions when listing files.
        Scenario: When the S3 service raises an exception.
        Expected outcome: An HTTPException with status code 500.
        Edge cases: Ensure that any exception leads to the same HTTP status.
        """
        mock_s3_service.list_files_in_s3.side_effect = Exception("Service error")
        with pytest.raises(HTTPException) as exc_info:
            await list_files()
        assert exc_info.value.status_code == 500, "Expected status code 500 for internal server error."
        assert exc_info.value.detail == "Internal Server Error", "Expected specific error detail message."
    async def test_list_files_empty(self, mock_s3_service: MagicMock) -> None:
        """
        Purpose: Test the response when no files are found in S3.
        Scenario: When the S3 service returns an empty list.
        Expected outcome: A JSON response with status code 200 and an empty list.
        Edge cases: Verify the output structure even when no files exist.
        """
        mock_s3_service.list_files_in_s3.return_value = []
        response: JSONResponse = await list_files()
        assert response.status_code == 200, "Expected status code 200 for empty file list."
        assert response.content == {"files": []}, "Expected response content to be an empty list."
if __name__ == "__main__":
    pytest.main()
