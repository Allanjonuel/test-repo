import pytest
from unittest.mock import MagicMock, patch
from typing import List
from src.fastapi_s3_app.app.services.s3_service import S3Service
from botocore.exceptions import NoCredentialsError, ClientError
@pytest.fixture(scope="class")
def s3_service() -> S3Service:
    """Fixture to create an instance of S3Service for testing."""
    with patch("boto3.client") as mock_client:
        yield S3Service(bucket_name="test-bucket")
@pytest.fixture
def mock_file() -> MagicMock:
    """Fixture to create a mock file object for upload tests."""
    mock_file = MagicMock()
    mock_file.file = MagicMock()
    mock_file.filename = "test_file.txt"
    return mock_file
@pytest.fixture
def mock_client(s3_service: S3Service) -> MagicMock:
    """Fixture to mock the S3 client methods for testing."""
    return s3_service.s3_client
class TestS3Service:
    """Test suite for S3Service class methods."""
    def test_upload_file_to_s3_success(self, s3_service: S3Service, mock_file: MagicMock, mock_client: MagicMock) -> None:
        """Test successful upload of a file to S3.
        Purpose:
            Verify that a file can be successfully uploaded to S3.
        Scenario:
            A valid file mock is provided to the upload_file_to_s3 method.
        Expected outcome:
            The method should return the correct URL of the uploaded file.
        Edge cases:
            None for this test case.
        """
        mock_client.upload_fileobj.return_value = None
        file_url = s3_service.upload_file_to_s3(mock_file)
        assert file_url == "https://test-bucket.s3.amazonaws.com/test_file.txt"
        mock_client.upload_fileobj.assert_called_once_with(mock_file.file, "test-bucket", mock_file.filename)
    def test_upload_file_to_s3_no_credentials(self, s3_service: S3Service, mock_file: MagicMock, mock_client: MagicMock) -> None:
        """Test upload failure due to missing AWS credentials.
        Purpose:
            Verify that the appropriate exception is raised when credentials are missing.
        Scenario:
            The upload_fileobj method raises NoCredentialsError.
        Expected outcome:
            An exception should be raised indicating no AWS credentials are available.
        Edge cases:
            None for this test case.
        """
        mock_client.upload_fileobj.side_effect = NoCredentialsError
        with pytest.raises(Exception, match="AWS credentials not available."):
            s3_service.upload_file_to_s3(mock_file)
    def test_upload_file_to_s3_client_error(self, s3_service: S3Service, mock_file: MagicMock, mock_client: MagicMock) -> None:
        """Test upload failure due to client error.
        Purpose:
            Verify that the appropriate exception is raised on a client error.
        Scenario:
            The upload_fileobj method raises ClientError.
        Expected outcome:
            An exception should be raised indicating the upload failed.
        Edge cases:
            None for this test case.
        """
        mock_client.upload_fileobj.side_effect = ClientError({"Error": {"Code": "500", "Message": "Internal Server Error"}}, "Upload")
        with pytest.raises(Exception, match="Failed to upload file."):
            s3_service.upload_file_to_s3(mock_file)
    def test_list_files_in_s3_success(self, s3_service: S3Service, mock_client: MagicMock) -> None:
        """Test successful listing of files in S3.
        Purpose:
            Verify that the method correctly lists files present in the S3 bucket.
        Scenario:
            The list_objects_v2 method returns a valid response with file keys.
        Expected outcome:
            The method should return a list of file names.
        Edge cases:
            None for this test case.
        """
        mock_client.list_objects_v2.return_value = {
            "Contents": [{"Key": "file1.txt"}, {"Key": "file2.txt"}]
        }
        files = s3_service.list_files_in_s3()
        assert files == ["file1.txt", "file2.txt"]
        mock_client.list_objects_v2.assert_called_once_with(Bucket="test-bucket")
    def test_list_files_in_s3_empty(self, s3_service: S3Service, mock_client: MagicMock) -> None:
        """Test listing files when S3 bucket is empty.
        Purpose:
            Verify that the method returns an empty list when there are no files in S3.
        Scenario:
            The list_objects_v2 method returns a response without contents.
        Expected outcome:
            The method should return an empty list.
        Edge cases:
            None for this test case.
        """
        mock_client.list_objects_v2.return_value = {}
        files = s3_service.list_files_in_s3()
        assert files == []
        mock_client.list_objects_v2.assert_called_once_with(Bucket="test-bucket")
    def test_list_files_in_s3_client_error(self, s3_service: S3Service, mock_client: MagicMock) -> None:
        """Test failure to list files due to client error.
        Purpose:
            Verify that the appropriate exception is raised on a client error.
        Scenario:
            The list_objects_v2 method raises ClientError.
        Expected outcome:
            An exception should be raised indicating the listing failed.
        Edge cases:
            None for this test case.
        """
        mock_client.list_objects_v2.side_effect = ClientError({"Error": {"Code": "500", "Message": "Internal Server Error"}}, "List")
        with pytest.raises(Exception, match="Failed to list files."):
            s3_service.list_files_in_s3()
    def test_get_file_from_s3_success(self, s3_service: S3Service, mock_client: MagicMock) -> None:
        """Test successful retrieval of a file from S3.
        Purpose:
            Verify that the method correctly retrieves a file from S3.
        Scenario:
            The get_object method returns a valid StreamingBody response.
        Expected outcome:
            The method should return the content of the file.
        Edge cases:
            None for this test case.
        """
        mock_response = {"Body": "file content"}
        mock_client.get_object.return_value = mock_response
        content = s3_service.get_file_from_s3("test_file.txt")
        assert content == "file content"
        mock_client.get_object.assert_called_once_with(Bucket="test-bucket", Key="test_file.txt")
    def test_get_file_from_s3_not_found(self, s3_service: S3Service, mock_client: MagicMock) -> None:
        """Test retrieval failure when file does not exist.
        Purpose:
            Verify that the appropriate exception is raised when the file is not found.
        Scenario:
            The get_object method raises NoSuchKey.
        Expected outcome:
            A FileNotFoundError should be raised.
        Edge cases:
            None for this test case.
        """
        mock_client.get_object.side_effect = s3_service.s3_client.exceptions.NoSuchKey
        with pytest.raises(FileNotFoundError, match="File test_file.txt not found."):
            s3_service.get_file_from_s3("test_file.txt")
    def test_get_file_from_s3_client_error(self, s3_service: S3Service, mock_client: MagicMock) -> None:
        """Test retrieval failure due to client error.
        Purpose:
            Verify that the appropriate exception is raised on a client error.
        Scenario:
            The get_object method raises ClientError.
        Expected outcome:
            An exception should be raised indicating the retrieval failed.
        Edge cases:
            None for this test case.
        """
        mock_client.get_object.side_effect = ClientError({"Error": {"Code": "500", "Message": "Internal Server Error"}}, "Get")
        with pytest.raises(Exception, match="Failed to retrieve file."):
            s3_service.get_file_from_s3("test_file.txt")
