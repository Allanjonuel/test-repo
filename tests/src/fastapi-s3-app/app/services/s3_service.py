"""Unit tests for the S3Service class in the S3 service module.
This test suite validates the functionality of the S3Service methods including
uploading files, listing files, and retrieving files from AWS S3. It ensures that
the methods behave as expected under normal conditions as well as in the presence
of errors.
"""
import pytest
from unittest.mock import MagicMock, patch
from src.fastapi_s3_app.app.services.s3_service import S3Service
from botocore.exceptions import NoCredentialsError, ClientError
from typing import Any
@pytest.fixture(scope="module")
def s3_service() -> S3Service:
    """Fixture that provides an instance of S3Service for tests.
    Returns:
        S3Service: An instance of the S3Service class.
    """
    return S3Service()
@pytest.fixture()
def mock_file() -> Any:
    """Fixture that simulates a file-like object for uploads.
    Returns:
        Any: A mock object representing a file with 'file' and 'filename' attributes.
    """
    mock_file = MagicMock()
    mock_file.file = MagicMock()
    mock_file.filename = "test_file.txt"
    return mock_file
class TestS3ServiceUpload:
    """Tests for the upload_file_to_s3 method of S3Service."""
    @patch('src.fastapi_s3_app.app.services.s3_service.boto3.client')
    def test_upload_file_success(self, mock_boto_client: MagicMock, s3_service: S3Service, mock_file: Any) -> None:
        """Test successful file upload to S3.
        Purpose: Verify that a file can be uploaded successfully.
        Scenario: Mock the S3 client to simulate successful upload.
        Expected outcome: The returned URL matches the expected S3 URL.
        """
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        result = s3_service.upload_file_to_s3(mock_file)
        assert result == "https://bucket-for-ai-generated-content.s3.amazonaws.com/test_file.txt"
        mock_s3.upload_fileobj.assert_called_once_with(mock_file.file, s3_service.bucket_name, mock_file.filename)
    @patch('src.fastapi_s3_app.app.services.s3_service.boto3.client')
    def test_upload_file_no_credentials(self, mock_boto_client: MagicMock, s3_service: S3Service, mock_file: Any) -> None:
        """Test upload failure due to missing AWS credentials.
        Purpose: Verify that the proper exception is raised when credentials are missing.
        Scenario: Raise NoCredentialsError when attempting to upload.
        Expected outcome: An exception indicating that credentials are not available is raised.
        """
        mock_s3 = MagicMock()
        mock_s3.upload_fileobj.side_effect = NoCredentialsError
        mock_boto_client.return_value = mock_s3
        with pytest.raises(Exception, match="AWS credentials not available."):
            s3_service.upload_file_to_s3(mock_file)
    @patch('src.fastapi_s3_app.app.services.s3_service.boto3.client')
    def test_upload_file_client_error(self, mock_boto_client: MagicMock, s3_service: S3Service, mock_file: Any) -> None:
        """Test upload failure due to client error.
        Purpose: Ensure that an exception is raised when S3 client encounters an error.
        Scenario: Raise ClientError when attempting to upload.
        Expected outcome: An exception with a generic upload error message is raised.
        """
        mock_s3 = MagicMock()
        mock_s3.upload_fileobj.side_effect = ClientError({"Error": {"Code": "InternalError"}}, "PutObject")
        mock_boto_client.return_value = mock_s3
        with pytest.raises(Exception, match="Failed to upload file."):
            s3_service.upload_file_to_s3(mock_file)
class TestS3ServiceList:
    """Tests for the list_files_in_s3 method of S3Service."""
    @patch('src.fastapi_s3_app.app.services.s3_service.boto3.client')
    def test_list_files_success(self, mock_boto_client: MagicMock, s3_service: S3Service) -> None:
        """Test successful retrieval of file list from S3.
        Purpose: Verify that the list of files can be retrieved successfully.
        Scenario: Mock the S3 client to return a list of files.
        Expected outcome: The returned list matches the mocked file list.
        """
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        mock_s3.list_objects_v2.return_value = {'Contents': [{'Key': 'file1.txt'}, {'Key': 'file2.txt'}]}
        result = s3_service.list_files_in_s3()
        assert result == ['file1.txt', 'file2.txt']
        mock_s3.list_objects_v2.assert_called_once_with(Bucket=s3_service.bucket_name)
    @patch('src.fastapi_s3_app.app.services.s3_service.boto3.client')
    def test_list_files_empty(self, mock_boto_client: MagicMock, s3_service: S3Service) -> None:
        """Test listing files when no files are present in S3.
        Purpose: Ensure that an empty list is returned when no files exist.
        Scenario: Mock the S3 client to return no contents.
        Expected outcome: An empty list is returned.
        """
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        mock_s3.list_objects_v2.return_value = {}
        result = s3_service.list_files_in_s3()
        assert result == []
        mock_s3.list_objects_v2.assert_called_once_with(Bucket=s3_service.bucket_name)
    @patch('src.fastapi_s3_app.app.services.s3_service.boto3.client')
    def test_list_files_client_error(self, mock_boto_client: MagicMock, s3_service: S3Service) -> None:
        """Test listing files failure due to client error.
        Purpose: Verify that an exception is raised when S3 client encounters an error.
        Scenario: Raise ClientError when attempting to list files.
        Expected outcome: An exception with a generic listing error message is raised.
        """
        mock_s3 = MagicMock()
        mock_s3.list_objects_v2.side_effect = ClientError({"Error": {"Code": "InternalError"}}, "ListObjects")
        mock_boto_client.return_value = mock_s3
        with pytest.raises(Exception, match="Failed to list files."):
            s3_service.list_files_in_s3()
class TestS3ServiceGet:
    """Tests for the get_file_from_s3 method of S3Service."""
    @patch('src.fastapi_s3_app.app.services.s3_service.boto3.client')
    def test_get_file_success(self, mock_boto_client: MagicMock, s3_service: S3Service) -> None:
        """Test successful retrieval of a file from S3.
        Purpose: Ensure that a file can be retrieved successfully.
        Scenario: Mock the S3 client to return a file object.
        Expected outcome: The retrieved object matches the mock file body.
        """
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        mock_response = {'Body': 'mock file content'}
        mock_s3.get_object.return_value = mock_response
        result = s3_service.get_file_from_s3('test_file.txt')
        assert result == 'mock file content'
        mock_s3.get_object.assert_called_once_with(Bucket=s3_service.bucket_name, Key='test_file.txt')
    @patch('src.fastapi_s3_app.app.services.s3_service.boto3.client')
    def test_get_file_not_found(self, mock_boto_client: MagicMock, s3_service: S3Service) -> None:
        """Test retrieval failure due to file not found.
        Purpose: Verify that a FileNotFoundError is raised when the file does not exist.
        Scenario: Raise NoSuchKey when attempting to retrieve a non-existing file.
        Expected outcome: A FileNotFoundError is raised with an appropriate message.
        """
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        mock_s3.get_object.side_effect = mock_s3.exceptions.NoSuchKey
        with pytest.raises(FileNotFoundError, match="File test_file.txt not found."):
            s3_service.get_file_from_s3('test_file.txt')
    @patch('src.fastapi_s3_app.app.services.s3_service.boto3.client')
    def test_get_file_client_error(self, mock_boto_client: MagicMock, s3_service: S3Service) -> None:
        """Test retrieval failure due to client error.
        Purpose: Ensure that an exception is raised when S3 client encounters an error.
        Scenario: Raise ClientError when attempting to retrieve a file.
        Expected outcome: An exception with a generic retrieval error message is raised.
        """
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        mock_s3.get_object.side_effect = ClientError({"Error": {"Code": "InternalError"}}, "GetObject")
        with pytest.raises(Exception, match="Failed to retrieve file."):
            s3_service.get_file_from_s3('test_file.txt')
