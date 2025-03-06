import pytest
from unittest.mock import MagicMock, patch
from typing import List
from src.fastapi_s3_app.app.services.s3_service import S3Service
from botocore.exceptions import NoCredentialsError, ClientError
@pytest.fixture(scope="class")
def s3_service() -> S3Service:
    """Fixture for S3Service to be used in tests."""
    with patch("boto3.client") as mock_client:
        yield S3Service(bucket_name="test-bucket")
@pytest.fixture
def mock_file() -> MagicMock:
    """Fixture for a mock file object used in upload tests."""
    file_mock = MagicMock()
    file_mock.file = MagicMock()
    file_mock.filename = "test_file.txt"
    return file_mock
@pytest.mark.usefixtures("s3_service")
class TestS3Service:
    """Test suite for S3Service class methods."""
    def test_upload_file_to_s3_success(self, s3_service: S3Service, mock_file: MagicMock) -> None:
        """Test successful file upload to S3.
        Scenario: A valid file is uploaded to the S3 bucket.
        Expected outcome: The file URL is returned successfully.
        """
        s3_service.s3_client.upload_fileobj = MagicMock()
        result = s3_service.upload_file_to_s3(mock_file)
        assert result == "https://test-bucket.s3.amazonaws.com/test_file.txt"
        s3_service.s3_client.upload_fileobj.assert_called_once_with(mock_file.file, "test-bucket", "test_file.txt")
    def test_upload_file_to_s3_no_credentials(self, s3_service: S3Service, mock_file: MagicMock) -> None:
        """Test upload file to S3 raises exception when credentials are missing.
        Scenario: AWS credentials are not available.
        Expected outcome: An exception is raised indicating no credentials.
        """
        s3_service.s3_client.upload_fileobj = MagicMock(side_effect=NoCredentialsError)
        with pytest.raises(Exception, match="AWS credentials not available."):
            s3_service.upload_file_to_s3(mock_file)
    def test_upload_file_to_s3_client_error(self, s3_service: S3Service, mock_file: MagicMock) -> None:
        """Test upload file to S3 raises exception on ClientError.
        Scenario: An error occurs during the file upload process.
        Expected outcome: An exception is raised indicating upload failure.
        """
        s3_service.s3_client.upload_fileobj = MagicMock(side_effect=ClientError({}, 'PutObject'))
        with pytest.raises(Exception, match="Failed to upload file."):
            s3_service.upload_file_to_s3(mock_file)
    def test_list_files_in_s3_success(self, s3_service: S3Service) -> None:
        """Test listing files in S3 bucket successfully.
        Scenario: The S3 bucket contains files.
        Expected outcome: A list of file names is returned.
        """
        s3_service.s3_client.list_objects_v2 = MagicMock(return_value={
            'Contents': [{'Key': 'file1.txt'}, {'Key': 'file2.txt'}]
        })
        result = s3_service.list_files_in_s3()
        assert result == ['file1.txt', 'file2.txt']
    def test_list_files_in_s3_empty(self, s3_service: S3Service) -> None:
        """Test listing files in S3 bucket when empty.
        Scenario: The S3 bucket does not contain any files.
        Expected outcome: An empty list is returned.
        """
        s3_service.s3_client.list_objects_v2 = MagicMock(return_value={})
        result = s3_service.list_files_in_s3()
        assert result == []
    def test_list_files_in_s3_client_error(self, s3_service: S3Service) -> None:
        """Test listing files in S3 raises exception on ClientError.
        Scenario: An error occurs while listing files.
        Expected outcome: An exception is raised indicating failure to list files.
        """
        s3_service.s3_client.list_objects_v2 = MagicMock(side_effect=ClientError({}, 'ListObjectsV2'))
        with pytest.raises(Exception, match="Failed to list files."):
            s3_service.list_files_in_s3()
    def test_get_file_from_s3_success(self, s3_service: S3Service) -> None:
        """Test retrieving a file from S3 successfully.
        Scenario: A file exists in the S3 bucket.
        Expected outcome: The file content is returned successfully.
        """
        mock_body = MagicMock()
        s3_service.s3_client.get_object = MagicMock(return_value={'Body': mock_body})
        result = s3_service.get_file_from_s3("existing_file.txt")
        assert result == mock_body
    def test_get_file_from_s3_file_not_found(self, s3_service: S3Service) -> None:
        """Test retrieving a file from S3 raises FileNotFoundError.
        Scenario: The requested file does not exist in the S3 bucket.
        Expected outcome: A FileNotFoundError is raised indicating the file is not found.
        """
        s3_service.s3_client.get_object = MagicMock(side_effect=s3_service.s3_client.exceptions.NoSuchKey)
        with pytest.raises(FileNotFoundError, match="File existing_file.txt not found."):
            s3_service.get_file_from_s3("existing_file.txt")
    def test_get_file_from_s3_client_error(self, s3_service: S3Service) -> None:
        """Test retrieving a file from S3 raises exception on ClientError.
        Scenario: An error occurs while retrieving the file.
        Expected outcome: An exception is raised indicating failure to retrieve the file.
        """
        s3_service.s3_client.get_object = MagicMock(side_effect=ClientError({}, 'GetObject'))
        with pytest.raises(Exception, match="Failed to retrieve file."):
            s3_service.get_file_from_s3("existing_file.txt")
