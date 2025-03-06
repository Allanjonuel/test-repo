"""Test suite for the upload functionality in the FastAPI S3 application."""
import pytest
from typing import Any
from fastapi import UploadFile, HTTPException
from fastapi.responses import JSONResponse
from src.fastapi_s3_app.app.routers.upload import upload_file
from unittest.mock import AsyncMock, patch
from io import BytesIO
@pytest.fixture
def mock_s3_service() -> Any:
    """Fixture to mock the S3Service for testing."""
    with patch("src.fastapi_s3_app.app.routers.upload.S3Service") as mock:
        yield mock
@pytest.fixture
def mock_validate_file_type() -> Any:
    """Fixture to mock the validate_file_type function."""
    with patch("src.fastapi_s3_app.app.routers.upload.validate_file_type") as mock:
        yield mock
@pytest.fixture
def mock_validate_file_size() -> Any:
    """Fixture to mock the validate_file_size function."""
    with patch("src.fastapi_s3_app.app.routers.upload.validate_file_size") as mock:
        yield mock
@pytest.fixture
def test_file() -> UploadFile:
    """Fixture to create a test UploadFile object."""
    file_content = BytesIO(b"test file content")
    file_content.name = "test_file.txt"
    return UploadFile(file=file_content, filename=file_content.name)
class TestUploadFile:
    """Test class for the upload_file function."""
    @pytest.mark.asyncio
    async def test_upload_file_success(self, mock_s3_service: Any, mock_validate_file_type: Any,
                                        mock_validate_file_size: Any, test_file: UploadFile) -> None:
        """Test successful file upload to S3.
        Purpose: Verify that a file can be uploaded successfully.
        Scenario: A valid file is provided for upload.
        Expected outcome: A JSON response with a success message and file URL.
        """
        mock_validate_file_type.return_value = None
        mock_validate_file_size.return_value = None
        mock_s3_service.return_value.upload_file_to_s3.return_value = "http://example.com/test_file.txt"
        response = await upload_file(test_file)
        assert response.status_code == 200
        assert response.content.decode() == '{"message":"File uploaded successfully","file_url":"http://example.com/test_file.txt"}'
    @pytest.mark.asyncio
    async def test_upload_file_validation_error(self, mock_s3_service: Any,
                                                 mock_validate_file_size: Any,
                                                 test_file: UploadFile) -> None:
        """Test file upload with validation error.
        Purpose: Ensure the function raises an HTTPException for validation errors.
        Scenario: A file fails validation for file type.
        Expected outcome: An HTTPException with status code 400.
        """
        mock_validate_file_size.return_value = None
        mock_s3_service.return_value.upload_file_to_s3.return_value = "http://example.com/test_file.txt"
        with patch("src.fastapi_s3_app.app.routers.upload.validate_file_type", side_effect=ValueError("Invalid file type")):
            with pytest.raises(HTTPException) as exc_info:
                await upload_file(test_file)
            assert exc_info.value.status_code == 400
            assert str(exc_info.value.detail) == "Invalid file type"
    @pytest.mark.asyncio
    async def test_upload_file_internal_server_error(self, mock_s3_service: Any,
                                                      mock_validate_file_type: Any,
                                                      mock_validate_file_size: Any,
                                                      test_file: UploadFile) -> None:
        """Test file upload with internal server error.
        Purpose: Verify that an HTTPException is raised for unexpected errors.
        Scenario: An unexpected error occurs during file upload.
        Expected outcome: An HTTPException with status code 500.
        """
        mock_validate_file_type.return_value = None
        mock_validate_file_size.return_value = None
        mock_s3_service.return_value.upload_file_to_s3.side_effect = Exception("S3 upload failed")
        with pytest.raises(HTTPException) as exc_info:
            await upload_file(test_file)
        assert exc_info.value.status_code == 500
        assert str(exc_info.value.detail) == "Internal Server Error"
    @pytest.mark.asyncio
    async def test_upload_file_size_validation_error(self, mock_s3_service: Any,
                                                      mock_validate_file_type: Any,
                                                      test_file: UploadFile) -> None:
        """Test file upload with size validation error.
        Purpose: Ensure the function raises an HTTPException for size validation errors.
        Scenario: A file exceeds the maximum allowed size.
        Expected outcome: An HTTPException with status code 400.
        """
        with patch("src.fastapi_s3_app.app.routers.upload.validate_file_size", side_effect=ValueError("File too large")):
            with pytest.raises(HTTPException) as exc_info:
                await upload_file(test_file)
            assert exc_info.value.status_code == 400
            assert str(exc_info.value.detail) == "File too large"
    @pytest.mark.asyncio
    async def test_upload_file_type_validation_error(self, mock_s3_service: Any,
                                                      test_file: UploadFile) -> None:
        """Test file upload with type validation error.
        Purpose: Ensure the function raises an HTTPException for type validation errors.
        Scenario: A file provided is of an unsupported type.
        Expected outcome: An HTTPException with status code 400.
        """
        with patch("src.fastapi_s3_app.app.routers.upload.validate_file_type", side_effect=ValueError("Unsupported file type")):
            with pytest.raises(HTTPException) as exc_info:
                await upload_file(test_file)
            assert exc_info.value.status_code == 400
            assert str(exc_info.value.detail) == "Unsupported file type"
    @pytest.mark.asyncio
    async def test_upload_file_without_file(self) -> None:
        """Test upload_file function when no file is provided.
        Purpose: Ensure the function raises an HTTPException when no file is attached.
        Scenario: The upload_file function is called without a file.
        Expected outcome: An HTTPException with status code 422.
        """
        with pytest.raises(HTTPException) as exc_info:
            await upload_file()
        assert exc_info.value.status_code == 422
