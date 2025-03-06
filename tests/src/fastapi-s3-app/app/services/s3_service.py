import pytest
from unittest.mock import MagicMock, patch
from typing import Any, List
from src.fastapi_s3_app.app.services.s3_service import S3Service
@pytest.fixture(scope='function')
def s3_service() -> S3Service:
    """Fixture for initializing S3Service with mocked boto3 client."""
    with patch('boto3.client') as mock_client:
        yield S3Service(bucket_name='test-bucket')
@pytest.fixture
def mock_file() -> Any:
    """Fixture for creating a mock file object."""
    mock_file = MagicMock()
    mock_file.file = MagicMock()
    mock_file.filename = 'test_file.txt'
    return mock_file
class TestS3ServiceUpload:
    """Test suite for the upload_file_to_s3 method in S3Service."""
    def test_upload_file_success(self, s3_service: S3Service, mock_file: Any) -> None:
        """Tests successful file upload to S3.
        Scenario: A valid file is uploaded to the S3 bucket.
        Expected outcome: The file URL is returned.
        Edge cases: None.
        """
        s3_service.s3_client.upload_fileobj = MagicMock()
        expected_url = 'https://test-bucket.s3.amazonaws.com/test_file.txt'
        result = s3_service.upload_file_to_s3(mock_file)
        assert result == expected_url
        s3_service.s3_client.upload_fileobj.assert_called_once_with(mock_file.file, s3_service.bucket_name, mock_file.filename)
    def test_upload_file_no_credentials_error(self, s3_service: S3Service, mock_file: Any) -> None:
        """Tests handling of NoCredentialsError during file upload.
        Scenario: AWS credentials are not available.
        Expected outcome: An exception is raised with the appropriate message.
        Edge cases: None.
        """
        s3_service.s3_client.upload_fileobj.side_effect = NoCredentialsError
        with pytest.raises(Exception, match="AWS credentials not available."):
            s3_service.upload_file_to_s3(mock_file)
    def test_upload_file_client_error(self, s3_service: S3Service, mock_file: Any) -> None:
        """Tests handling of ClientError during file upload.
        Scenario: An unexpected ClientError occurs.
        Expected outcome: An exception is raised with the appropriate message.
        Edge cases: None.
        """
        s3_service.s3_client.upload_fileobj.side_effect = ClientError({}, 'Upload')
        with pytest.raises(Exception, match="Failed to upload file."):
            s3_service.upload_file_to_s3(mock_file)
class TestS3ServiceList:
    """Test suite for the list_files_in_s3 method in S3Service."""
    def test_list_files_success(self, s3_service: S3Service) -> None:
        """Tests successful listing of files in S3.
        Scenario: There are files present in the S3 bucket.
        Expected outcome: A list of filenames is returned.
        Edge cases: None.
        """
        s3_service.s3_client.list_objects_v2 = MagicMock(return_value={'Contents': [{'Key': 'file1.txt'}, {'Key': 'file2.txt'}]})
        result = s3_service.list_files_in_s3()
        assert result == ['file1.txt', 'file2.txt']
    def test_list_files_empty(self, s3_service: S3Service) -> None:
        """Tests listing files when no files are present in S3.
        Scenario: The S3 bucket is empty.
        Expected outcome: An empty list is returned.
        Edge cases: None.
        """
        s3_service.s3_client.list_objects_v2 = MagicMock(return_value={})
        result = s3_service.list_files_in_s3()
        assert result == []
    def test_list_files_client_error(self, s3_service: S3Service) -> None:
        """Tests handling of ClientError during listing files.
        Scenario: An unexpected ClientError occurs.
        Expected outcome: An exception is raised with the appropriate message.
        Edge cases: None.
        """
        s3_service.s3_client.list_objects_v2.side_effect = ClientError({}, 'List')
        with pytest.raises(Exception, match="Failed to list files."):
            s3_service.list_files_in_s3()
class TestS3ServiceGetFile:
    """Test suite for the get_file_from_s3 method in S3Service."""
    def test_get_file_success(self, s3_service: S3Service) -> None:
        """Tests successful retrieval of a file from S3.
        Scenario: The specified file exists in the S3 bucket.
        Expected outcome: The file content is returned.
        Edge cases: None.
        """
        file_content_mock = MagicMock()
        s3_service.s3_client.get_object = MagicMock(return_value={'Body': file_content_mock})
        result = s3_service.get_file_from_s3('existing_file.txt')
        assert result == file_content_mock
    def test_get_file_not_found_error(self, s3_service: S3Service) -> None:
        """Tests handling of NoSuchKey error when retrieving a file.
        Scenario: The specified file does not exist.
        Expected outcome: A FileNotFoundError is raised with the appropriate message.
        Edge cases: None.
        """
        s3_service.s3_client.get_object.side_effect = s3_service.s3_client.exceptions.NoSuchKey
        with pytest.raises(FileNotFoundError, match="File existing_file.txt not found."):
            s3_service.get_file_from_s3('existing_file.txt')
    def test_get_file_client_error(self, s3_service: S3Service) -> None:
        """Tests handling of ClientError during file retrieval.
        Scenario: An unexpected ClientError occurs.
        Expected outcome: An exception is raised with the appropriate message.
        Edge cases: None.
        """
        s3_service.s3_client.get_object.side_effect = ClientError({}, 'Get')
        with pytest.raises(Exception, match="Failed to retrieve file."):
            s3_service.get_file_from_s3('existing_file.txt')
