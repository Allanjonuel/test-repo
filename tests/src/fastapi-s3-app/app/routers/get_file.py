"""
Test suite for the get_file function in the FastAPI S3 application.
This module tests the endpoint responsible for retrieving files from an S3 bucket.
It ensures that the function behaves correctly under various conditions, including
successful retrieval, file not found, and other exceptions.
"""
import pytest
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from src.fastapi_s3_app.app.routers.get_file import get_file
from unittest.mock import AsyncMock, patch
from typing import Any
@pytest.fixture(scope="module")
def mock_s3_service() -> Any:
    """Fixture to mock the S3Service for testing."""
    with patch("src.fastapi_s3_app.app.routers.get_file.s3_service") as mock_service:
        yield mock_service
@pytest.mark.asyncio
class TestGetFile:
    """Test cases for the get_file endpoint."""
    @pytest.mark.parametrize("file_name, expected_media_type", [
        ("valid_file.txt", "application/octet-stream"),
    ])
    async def test_get_file_success(self, mock_s3_service: Any, file_name: str, expected_media_type: str) -> None:
        """
        Purpose: Test successful retrieval of a file from S3.
        Scenario: Providing a valid file name that exists in S3.
        Expected outcome: The response is a StreamingResponse with the correct media type.
        Edge cases: None.
        """
        mock_s3_service.get_file_from_s3 = AsyncMock(return_value=b"file content")
        response = await get_file(file_name)
        assert isinstance(response, StreamingResponse), f"Expected StreamingResponse but got {type(response)}"
        assert response.media_type == expected_media_type, f"Expected media type '{expected_media_type}' but got '{response.media_type}'"
    @pytest.mark.asyncio
    async def test_get_file_not_found(self, mock_s3_service: Any) -> None:
        """
        Purpose: Test behavior when the file is not found in S3.
        Scenario: Providing a file name that does not exist in S3.
        Expected outcome: The function raises HTTPException with a 404 status code.
        Edge cases: None.
        """
        mock_s3_service.get_file_from_s3 = AsyncMock(side_effect=FileNotFoundError)
        with pytest.raises(HTTPException) as exc_info:
            await get_file("non_existent_file.txt")
        assert exc_info.value.status_code == 404, f"Expected status code 404 but got {exc_info.value.status_code}"
        assert str(exc_info.value.detail) == "File not found", f"Expected error detail 'File not found' but got '{exc_info.value.detail}'"
    @pytest.mark.asyncio
    async def test_get_file_internal_server_error(self, mock_s3_service: Any) -> None:
        """
        Purpose: Test behavior when an unexpected error occurs while retrieving the file.
        Scenario: Simulating an unexpected exception during file retrieval.
        Expected outcome: The function raises HTTPException with a 500 status code.
        Edge cases: None.
        """
        mock_s3_service.get_file_from_s3 = AsyncMock(side_effect=Exception("Unexpected error"))
        with pytest.raises(HTTPException) as exc_info:
            await get_file("any_file.txt")
        assert exc_info.value.status_code == 500, f"Expected status code 500 but got {exc_info.value.status_code}"
        assert str(exc_info.value.detail) == "Internal Server Error", f"Expected error detail 'Internal Server Error' but got '{exc_info.value.detail}'"
    @pytest.mark.asyncio
    async def test_get_file_invalid_file_name(self, mock_s3_service: Any) -> None:
        """
        Purpose: Test behavior when an invalid file name is provided.
        Scenario: Providing an invalid file name that could cause exceptions.
        Expected outcome: The function raises HTTPException with a 500 status code.
        Edge cases: None.
        """
        mock_s3_service.get_file_from_s3 = AsyncMock(side_effect=Exception("Invalid file name"))
        with pytest.raises(HTTPException) as exc_info:
            await get_file("")
        assert exc_info.value.status_code == 500, f"Expected status code 500 but got {exc_info.value.status_code}"
        assert str(exc_info.value.detail) == "Internal Server Error", f"Expected error detail 'Internal Server Error' but got '{exc_info.value.detail}'"
