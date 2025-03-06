"""Test suite for the upload module in the FastAPI S3 application.
This module contains tests for the upload_file endpoint, which handles file uploads
to an S3 bucket. The tests cover successful uploads, validation errors, and other
exception scenarios to ensure robustness and reliability of the endpoint.
"""
import pytest
from fastapi import UploadFile, HTTPException
from fastapi.responses import JSONResponse
from unittest.mock import patch, MagicMock
from src.fastapi_s3_app.app.routers.upload import upload_file
from app.utils.validation import validate_file_type, validate_file_size
@pytest.fixture
def mock_s3_service() -> MagicMock:
    """Fixture for mocking the S3 service."""
    with patch('app.services.s3_service.S3Service') as mock:
        yield mock
@pytest.fixture
def valid_file() -> UploadFile:
    """Fixture for creating a valid UploadFile instance."""
    return UploadFile(filename='test_file.txt', file=MagicMock(), content_type='text/plain')
@pytest.fixture
def invalid_file() -> UploadFile:
    """Fixture for creating an invalid UploadFile instance."""
    return UploadFile(filename='test_file.exe', file=MagicMock(), content_type='application/octet-stream')
class TestUploadFile:
    """Test cases for the upload_file function."""
    @pytest.mark.asyncio
    @patch('app.utils.validation.validate_file_type')
    @patch('app.utils.validation.validate_file_size')
    async def test_upload_file_success(self, mock_validate_file_size, mock_validate_file_type, mock_s3_service, valid_file: UploadFile) -> None:
        """Test successful file upload.
        Purpose: To test the upload_file function with a valid file.
        Scenario: A valid file is uploaded, and the S3 service successfully uploads it.
        Expected outcome: The function returns a JSONResponse with a success message and file URL.
        """
        mock_validate_file_type.return_value = None
        mock_validate_file_size.return_value = None
        mock_s3_service.return_value.upload_file_to_s3.return_value = "http://example.com/test_file.txt"
        response = await upload_file(valid_file)
        assert isinstance(response, JSONResponse), "Response should be a JSONResponse"
        assert response.status_code == 200, "Status code should be 200"
        assert response.content['message'] == "File uploaded successfully", "Success message should match"
        assert response.content['file_url'] == "http://example.com/test_file.txt", "File URL should match"
    @pytest.mark.asyncio
    @patch('app.utils.validation.validate_file_type')
    @patch('app.utils.validation.validate_file_size')
    async def test_upload_file_validation_error(self, mock_validate_file_size, mock_validate_file_type, invalid_file: UploadFile) -> None:
        """Test file upload with validation error.
        Purpose: To test the upload_file function when file validation fails.
        Scenario: An invalid file type is uploaded.
        Expected outcome: The function raises an HTTPException with a 400 status code.
        """
        mock_validate_file_type.side_effect = ValueError("Invalid file type.")
        mock_validate_file_size.return_value = None
        with pytest.raises(HTTPException) as exc_info:
            await upload_file(invalid_file)
        assert exc_info.value.status_code == 400, "Status code should be 400"
        assert str(exc_info.value.detail) == "Invalid file type.", "Error message should match"
    @pytest.mark.asyncio
    @patch('app.utils.validation.validate_file_type')
    @patch('app.utils.validation.validate_file_size')
    async def test_upload_file_internal_error(self, mock_validate_file_size, mock_validate_file_type, valid_file: UploadFile, mock_s3_service: MagicMock) -> None:
        """Test file upload when an internal error occurs.
        Purpose: To test the upload_file function when an unexpected error occurs.
        Scenario: The S3 service raises an exception during upload.
        Expected outcome: The function raises an HTTPException with a 500 status code.
        """
        mock_validate_file_type.return_value = None
        mock_validate_file_size.return_value = None
        mock_s3_service.return_value.upload_file_to_s3.side_effect = Exception("S3 upload failed.")
        with pytest.raises(HTTPException) as exc_info:
            await upload_file(valid_file)
        assert exc_info.value.status_code == 500, "Status code should be 500"
        assert exc_info.value.detail == "Internal Server Error", "Error message should match"
    @pytest.mark.asyncio
    @patch('app.utils.validation.validate_file_type')
    @patch('app.utils.validation.validate_file_size')
    async def test_upload_file_size_validation(self, mock_validate_file_size, mock_validate_file_type, valid_file: UploadFile) -> None:
        """Test file upload with file size validation.
        Purpose: To test the upload_file function when file size exceeds the limit.
        Scenario: A valid file exceeds the allowed size during validation.
        Expected outcome: The function raises an HTTPException with a 400 status code.
        """
        mock_validate_file_type.return_value = None
        mock_validate_file_size.side_effect = ValueError("File size exceeds limit.")
        with pytest.raises(HTTPException) as exc_info:
            await upload_file(valid_file)
        assert exc_info.value.status_code == 400, "Status code should be 400"
        assert str(exc_info.value.detail) == "File size exceeds limit.", "Error message should match"
    @pytest.mark.asyncio
    @patch('app.utils.validation.validate_file_type')
    @patch('app.utils.validation.validate_file_size')
    async def test_upload_file_type_validation(self, mock_validate_file_size, mock_validate_file_type, invalid_file: UploadFile) -> None:
        """Test file upload with file type validation.
        Purpose: To test the upload_file function when file type is invalid.
        Scenario: An invalid file type is uploaded.
        Expected outcome: The function raises an HTTPException with a 400 status code.
        """
        mock_validate_file_type.side_effect = ValueError("Invalid file type.")
        mock_validate_file_size.return_value = None
        with pytest.raises(HTTPException) as exc_info:
            await upload_file(invalid_file)
        assert exc_info.value.status_code == 400, "Status code should be 400"
        assert str(exc_info.value.detail) == "Invalid file type.", "Error message should match"
    @pytest.mark.asyncio
    @patch('app.utils.validation.validate_file_type')
    @patch('app.utils.validation.validate_file_size')
    async def test_upload_file_empty_file(self, mock_validate_file_size, mock_validate_file_type) -> None:
        """Test file upload with an empty file.
        Purpose: To test the upload_file function when an empty file is uploaded.
        Scenario: An empty UploadFile instance is passed.
        Expected outcome: The function raises an HTTPException with a 400 status code.
        """
        empty_file = UploadFile(filename='', file=MagicMock(), content_type='')
        mock_validate_file_type.return_value = None
        mock_validate_file_size.return_value = None
        with pytest.raises(HTTPException) as exc_info:
            await upload_file(empty_file)
        assert exc_info.value.status_code == 400, "Status code should be 400"
        assert str(exc_info.value.detail) == "File is required.", "Error message should match"
    @pytest.mark.asyncio
    @patch('app.utils.validation.validate_file_type')
    @patch('app.utils.validation.validate_file_size')
    async def test_upload_file_large_file(self, mock_validate_file_size, mock_validate_file_type, valid_file: UploadFile) -> None:
        """Test file upload with a large file.
        Purpose: To test the upload_file function when a large file is uploaded.
        Scenario: A valid but large file is uploaded that exceeds the allowed size.
        Expected outcome: The function raises an HTTPException with a 400 status code.
        """
        mock_validate_file_type.return_value = None
        mock_validate_file_size.side_effect = ValueError("File size exceeds limit.")
        with pytest.raises(HTTPException) as exc_info:
            await upload_file(valid_file)
        assert exc_info.value.status_code == 400, "Status code should be 400"
        assert str(exc_info.value.detail) == "File size exceeds limit.", "Error message should match"
    @pytest.mark.asyncio
    @patch('app.utils.validation.validate_file_type')
    @patch('app.utils.validation.validate_file_size')
    async def test_upload_file_invalid_content_type(self, mock_validate_file_size, mock_validate_file_type, invalid_file: UploadFile) -> None:
        """Test file upload with an invalid content type.
        Purpose: To test the upload_file function when the file has an invalid content type.
        Scenario: An invalid content type is provided during upload.
        Expected outcome: The function raises an HTTPException with a 400 status code.
        """
        mock_validate_file_type.side_effect = ValueError("Invalid content type.")
        mock_validate_file_size.return_value = None
        with pytest.raises(HTTPException) as exc_info:
            await upload_file(invalid_file)
        assert exc_info.value.status_code == 400, "Status code should be 400"
        assert str(exc_info.value.detail) == "Invalid content type.", "Error message should match"
    @pytest.mark.asyncio
    @patch('app.utils.validation.validate_file_type')
    @patch('app.utils.validation.validate_file_size')
    async def test_upload_file_no_file(self, mock_validate_file_size, mock_validate_file_type) -> None:
        """Test file upload with no file provided.
        Purpose: To test the upload_file function when no file is uploaded.
        Scenario: No file is included in the request.
        Expected outcome: The function raises an HTTPException with a 400 status code.
        """
        with pytest.raises(HTTPException) as exc_info:
            await upload_file(None)
        assert exc_info.value.status_code == 400, "Status code should be 400"
        assert str(exc_info.value.detail) == "File is required.", "Error message should match"
