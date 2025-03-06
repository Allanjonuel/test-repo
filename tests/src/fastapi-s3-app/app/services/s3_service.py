import pytest
from unittest.mock import MagicMock, patch
from src.fastapi_s3_app.app.services.s3_service import S3Service
from botocore.exceptions import NoCredentialsError, ClientError
from typing import Any
@pytest.fixture
def s3_service() -> S3Service:
    """Fixture for creating an instance of S3Service."""
    return S3Service(bucket_name="test-bucket")
@pytest.fixture
def mock_file() -> Any:
    """Fixture to mock a file-like object for testing."""
    mock_file_obj = MagicMock()
    mock_file_obj.file = MagicMock()
    mock_file_obj.filename = "test_file.txt"
    return mock_file_obj
@pytest.fixture
def mock_s3_client() -> None:
    """Fixture to mock the S3 client."""
    with patch("src.fastapi_s3_app.app.services.s3_service.boto3.client") as mock:
        yield mock
class TestS3Service:
    """Test suite for the S3Service class."""
    @pytest.fixture(autouse=True)
    def setup(self, mock_s3_client: None) -> None:
        """Setup the S3Service with a mocked S3 client."""
        self.service = S3Service(bucket_name="test-bucket")
    def test_upload_file_to_s3_success(self, mock_file: Any) -> None:
        """Test successful file upload to S3.
        Purpose: Ensure that a file can be uploaded successfully.
        Scenario: A valid file object is provided.
        Expected outcome: The URL of the uploaded file is returned.
        """
        mock_file.file = MagicMock()
        mock_file.filename = "test_file.txt"
        expected_url = "https://test-bucket.s3.amazonaws.com/test_file.txt"
        result = self.service.upload_file_to_s3(mock_file)
        assert result == expected_url, f"Expected URL {expected_url}, got {result}"
        self.service.s3_client.upload_fileobj.assert_called_once_with(mock_file.file, self.service.bucket_name, mock_file.filename)
    def test_upload_file_to_s3_no_credentials(self, mock_file: Any) -> None:
        """Test upload failure due to missing AWS credentials.
        Purpose: Ensure that an exception is raised when AWS credentials are not available.
        Scenario: NoCredentialsError is raised during upload.
        Expected outcome: An exception with the appropriate message is raised.
        """
        self.service.s3_client.upload_fileobj.side_effect = NoCredentialsError
        with pytest.raises(Exception, match="AWS credentials not available."):
            self.service.upload_file_to_s3(mock_file)
    def test_upload_file_to_s3_client_error(self, mock_file: Any) -> None:
        """Test upload failure due to a client error.
        Purpose: Ensure that an exception is raised on client errors.
        Scenario: ClientError is raised during file upload.
        Expected outcome: An exception with the appropriate message is raised.
        """
        self.service.s3_client.upload_fileobj.side_effect = ClientError({"Error": {"Code": "InternalError"}}, "Upload")
        with pytest.raises(Exception, match="Failed to upload file."):
            self.service.upload_file_to_s3(mock_file)
    def test_list_files_in_s3_success(self) -> None:
        """Test successful retrieval of file list from S3.
        Purpose: Ensure that files can be listed from the S3 bucket.
        Scenario: S3 returns a list of files.
        Expected outcome: A list of filenames is returned.
        """
        mock_response = {'Contents': [{'Key': 'file1.txt'}, {'Key': 'file2.txt'}]}
        self.service.s3_client.list_objects_v2.return_value = mock_response
        result = self.service.list_files_in_s3()
        expected_files = ['file1.txt', 'file2.txt']
        assert result == expected_files, f"Expected files {expected_files}, got {result}"
    def test_list_files_in_s3_no_files(self) -> None:
        """Test retrieval of file list when no files are present.
        Purpose: Ensure that an empty list is returned when no files exist.
        Scenario: S3 returns no contents.
        Expected outcome: An empty list is returned.
        """
        mock_response = {}
        self.service.s3_client.list_objects_v2.return_value = mock_response
        result = self.service.list_files_in_s3()
        assert result == [], "Expected an empty list, but got non-empty."
    def test_list_files_in_s3_client_error(self) -> None:
        """Test failure of file listing due to a client error.
        Purpose: Ensure that an exception is raised on client errors during listing.
        Scenario: ClientError is raised during file listing.
        Expected outcome: An exception with the appropriate message is raised.
        """
        self.service.s3_client.list_objects_v2.side_effect = ClientError({"Error": {"Code": "InternalError"}}, "List")
        with pytest.raises(Exception, match="Failed to list files."):
            self.service.list_files_in_s3()
    def test_get_file_from_s3_success(self) -> None:
        """Test successful retrieval of a file from S3.
        Purpose: Ensure that a file can be retrieved successfully.
        Scenario: A valid file name is provided.
        Expected outcome: The file content is returned.
        """
        mock_response = {'Body': "File content"}
        self.service.s3_client.get_object.return_value = mock_response
        result = self.service.get_file_from_s3("test_file.txt")
        assert result == mock_response['Body'], f"Expected file content, got {result}"
    def test_get_file_from_s3_not_found(self) -> None:
        """Test retrieval failure for a non-existent file.
        Purpose: Ensure that FileNotFoundError is raised when the file does not exist.
        Scenario: NoSuchKey exception is raised during retrieval.
        Expected outcome: A FileNotFoundError is raised with the correct message.
        """
        self.service.s3_client.get_object.side_effect = self.service.s3_client.exceptions.NoSuchKey
        with pytest.raises(FileNotFoundError, match="File test_file.txt not found."):
            self.service.get_file_from_s3("test_file.txt")
    def test_get_file_from_s3_client_error(self) -> None:
        """Test failure of file retrieval due to a client error.
        Purpose: Ensure that an exception is raised on client errors during retrieval.
        Scenario: ClientError is raised during file retrieval.
        Expected outcome: An exception with the appropriate message is raised.
        """
        self.service.s3_client.get_object.side_effect = ClientError({"Error": {"Code": "InternalError"}}, "Get")
        with pytest.raises(Exception, match="Failed to retrieve file."):
            self.service.get_file_from_s3("test_file.txt")
