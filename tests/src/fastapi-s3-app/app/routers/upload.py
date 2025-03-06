"""
Test suite for the upload functionality in the FastAPI S3 application.
This module contains tests for the upload_file endpoint, focusing on
validations, successful uploads, and error handling.
"""
import pytest
from typing import Any
from fastapi import UploadFile
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.fastapi_s3_app.app.routers.upload import router
@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """
    Fixture to create a FastAPI test client for testing the upload endpoint.
    Returns:
        TestClient: The FastAPI test client.
    """
    app = router
    return TestClient(app)
@pytest.fixture
def mock_s3_service() -> MagicMock:
    """
    Fixture to mock the S3Service used for file uploads.
    Returns:
        MagicMock: A mock instance of S3Service.
    """
    with patch("src.fastapi_s3_app.app.routers.upload.S3Service") as mock:
        yield mock
@pytest.fixture
def valid_file() -> UploadFile:
    """
    Fixture to create a valid UploadFile instance for testing.
    Returns:
        UploadFile: A valid UploadFile instance representing a dummy file.
    """
    file_content = b"dummy file content"
    file = UploadFile(filename="test_file.txt", file=MagicMock(read=lambda: file_content), content_type="text/plain")
    return file
@pytest.fixture
def invalid_file_type() -> UploadFile:
    """
    Fixture to create an invalid UploadFile instance for testing file type validation.
    Returns:
        UploadFile: An invalid UploadFile instance.
    """
    file_content = b"dummy file content"
    file = UploadFile(filename="test_file.exe", file=MagicMock(read=lambda: file_content), content_type="application/octet-stream")
    return file
@pytest.fixture
def invalid_file_size() -> UploadFile:
    """
    Fixture to create an invalid UploadFile instance for testing file size validation.
    Returns:
        UploadFile: An invalid UploadFile instance.
    """
    file_content = b"a" * (10 * 1024 * 1024 + 1)  # 10 MB + 1 byte
    file = UploadFile(filename="large_file.txt", file=MagicMock(read=lambda: file_content), content_type="text/plain")
    return file
@patch("src.fastapi_s3_app.app.routers.upload.validate_file_type")
@patch("src.fastapi_s3_app.app.routers.upload.validate_file_size")
@patch("src.fastapi_s3_app.app.routers.upload.s3_service.upload_file_to_s3")
def test_upload_file_success(mock_upload: MagicMock,
                             mock_validate_size: MagicMock,
                             mock_validate_type: MagicMock,
                             test_client: TestClient,
                             valid_file: UploadFile) -> None:
    """
    Test case for successfully uploading a valid file.
    Purpose: To ensure that the upload_file endpoint correctly handles a valid upload.
    Scenario: A valid file is uploaded.
    Expected outcome: A 200 response with a success message and file URL.
    """
    mock_validate_type.return_value = None
    mock_validate_size.return_value = None
    mock_upload.return_value = "http://mocked-url.com/test_file.txt"
    response = test_client.post("/upload/", files={"file": valid_file})
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully", "file_url": "http://mocked-url.com/test_file.txt"}
@patch("src.fastapi_s3_app.app.routers.upload.validate_file_type")
@patch("src.fastapi_s3_app.app.routers.upload.validate_file_size")
def test_upload_file_invalid_type(mock_validate_size: MagicMock,
                                   mock_validate_type: MagicMock,
                                   test_client: TestClient,
                                   invalid_file_type: UploadFile) -> None:
    """
    Test case for uploading a file with an invalid type.
    Purpose: To ensure that the upload_file endpoint raises an HTTPException for invalid file types.
    Scenario: An invalid file type is uploaded.
    Expected outcome: A 400 response with a validation error message.
    """
    mock_validate_type.side_effect = ValueError("Invalid file type.")
    mock_validate_size.return_value = None
    response = test_client.post("/upload/", files={"file": invalid_file_type})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file type."}
@patch("src.fastapi_s3_app.app.routers.upload.validate_file_type")
@patch("src.fastapi_s3_app.app.routers.upload.validate_file_size")
def test_upload_file_invalid_size(mock_validate_type: MagicMock,
                                   mock_validate_size: MagicMock,
                                   test_client: TestClient,
                                   invalid_file_size: UploadFile) -> None:
    """
    Test case for uploading a file that exceeds the allowed size.
    Purpose: To ensure that the upload_file endpoint raises an HTTPException for oversized files.
    Scenario: An oversized file is uploaded.
    Expected outcome: A 400 response with a validation error message.
    """
    mock_validate_type.return_value = None
    mock_validate_size.side_effect = ValueError("File size exceeds limit.")
    response = test_client.post("/upload/", files={"file": invalid_file_size})
    assert response.status_code == 400
    assert response.json() == {"detail": "File size exceeds limit."}
@patch("src.fastapi_s3_app.app.routers.upload.validate_file_type")
@patch("src.fastapi_s3_app.app.routers.upload.validate_file_size")
@patch("src.fastapi_s3_app.app.routers.upload.s3_service.upload_file_to_s3")
def test_upload_file_internal_error(mock_upload: MagicMock,
                                     mock_validate_size: MagicMock,
                                     mock_validate_type: MagicMock,
                                     test_client: TestClient,
                                     valid_file: UploadFile) -> None:
    """
    Test case for handling internal server error during file upload.
    Purpose: To ensure that the upload_file endpoint raises an HTTPException for internal errors.
    Scenario: An error occurs during the upload process.
    Expected outcome: A 500 response with an internal server error message.
    """
    mock_validate_type.return_value = None
    mock_validate_size.return_value = None
    mock_upload.side_effect = Exception("Upload failed.")
    response = test_client.post("/upload/", files={"file": valid_file})
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
