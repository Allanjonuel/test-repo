"""Unit tests for the list_files router in the FastAPI S3 application.
This module contains tests for the functionality of the list_files endpoint,
ensuring proper responses for both successful file listing and error conditions.
"""
import pytest
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from unittest.mock import AsyncMock, patch
from src.fastapi_s3_app.app.routers.list_files import router, list_files
from src.app.services.s3_service import S3Service
@pytest.fixture(scope="module")
def mock_s3_service():
    """Fixture to mock the S3Service for testing."""
    with patch("src.fastapi_s3_app.app.routers.list_files.S3Service") as MockS3Service:
        yield MockS3Service
@pytest.mark.asyncio
class TestListFiles:
    """Test cases for the list_files endpoint."""
    @pytest.fixture(autouse=True)
    def setup(self, mock_s3_service: AsyncMock):
        """Setup the mock S3 service before each test."""
        self.mock_service = mock_s3_service.return_value
        self.mock_service.list_files_in_s3 = AsyncMock()
    async def test_list_files_success(self) -> None:
        """Test successful retrieval of files from S3.
        Scenario: When the S3 service returns a list of files.
        Expected outcome: The response contains the list of files with a 200 status code.
        """
        expected_files = ["file1.txt", "file2.txt"]
        self.mock_service.list_files_in_s3.return_value = expected_files
        response = await list_files()
        assert response.status_code == 200, "Expected status code 200"
        assert response.content == '{"files":["file1.txt","file2.txt"]}', "Expected files list in response"
    async def test_list_files_failure(self) -> None:
        """Test failure in retrieving files from S3.
        Scenario: When the S3 service raises an exception.
        Expected outcome: An HTTPException is raised with a 500 status code.
        """
        self.mock_service.list_files_in_s3.side_effect = Exception("S3 service error")
        with pytest.raises(HTTPException) as exc:
            await list_files()
        assert exc.value.status_code == 500, "Expected status code 500"
        assert exc.value.detail == "Internal Server Error", "Expected error message"
    async def test_list_files_empty(self) -> None:
        """Test retrieval of an empty list of files from S3.
        Scenario: When the S3 service returns an empty list.
        Expected outcome: The response contains an empty list with a 200 status code.
        """
        expected_files = []
        self.mock_service.list_files_in_s3.return_value = expected_files
        response = await list_files()
        assert response.status_code == 200, "Expected status code 200"
        assert response.content == '{"files":[]}', "Expected empty files list in response"
    async def test_list_files_large_output(self) -> None:
        """Test handling of a large number of files from S3.
        Scenario: When the S3 service returns a large list of files.
        Expected outcome: The response contains the large list of files with a 200 status code.
        Edge cases: Testing the response size and handling.
        """
        expected_files = [f"file{i}.txt" for i in range(1000)]  # Simulate large output
        self.mock_service.list_files_in_s3.return_value = expected_files
        response = await list_files()
        assert response.status_code == 200, "Expected status code 200"
        assert response.content == f'{{"files":{expected_files}}}', "Expected large files list in response"
