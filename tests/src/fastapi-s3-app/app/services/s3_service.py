import pytest
from unittest.mock import MagicMock, patch
from src.fastapi_s3_app.app.services.s3_service import S3Service
from botocore.exceptions import NoCredentialsError, ClientError
from typing import Any, Dict, List
@pytest.fixture(scope='module')
def s3_service() -> S3Service:
    """Fixture for S3Service instance."""
    return S3Service(bucket_name='test-bucket')
@pytest.fixture
def mock_file() -> MagicMock:
    """Fixture for mocking a file object with filename and file attributes."""
    mock_file = MagicMock()
    mock_file.filename = 'test_file.txt'
    mock_file.file = MagicMock()  # Simulates a file-like object
    return mock_file
@pytest.fixture
def s3_client_mock() -> MagicMock:
    """Fixture for mocking the S3 client."""
    with patch('boto3.client') as mock:
        yield mock.return_value
class TestS3Service:
    """Test suite for S3Service class."""
    def test_upload_file_to_s3_success(self, s3_service: S3Service, mock_file: MagicMock, s3_client_mock: MagicMock) -> None:
        """Tests successful file upload to S3.
        Scenario: A valid file object is uploaded.
        Expected outcome: The function returns the correct file URL.
        """
        s3_client_mock.upload_fileobj.return_value = None  # Simulate successful upload
        file_url = s3_service.upload_file_to_s3(mock_file)
        assert file_url == "https://test-bucket.s3.amazonaws.com/test_file.txt"
        s3_client_mock.upload_fileobj.assert_called_once_with(mock_file.file, 'test-bucket', 'test_file.txt')
    def test_upload_file_to_s3_no_credentials(self, s3_service: S3Service, mock_file: MagicMock, s3_client_mock: MagicMock) -> None:
        """Tests upload failure due to missing AWS credentials.
        Scenario: AWS credentials are not available.
        Expected outcome: An exception is raised indicating the lack of credentials.
        """
        s3_client_mock.upload_fileobj.side_effect = NoCredentialsError
        with pytest.raises(Exception, match="AWS credentials not available."):
            s3_service.upload_file_to_s3(mock_file)
    def test_upload_file_to_s3_client_error(self, s3_service: S3Service, mock_file: MagicMock, s3_client_mock: MagicMock) -> None:
        """Tests upload failure due to a ClientError.
        Scenario: The upload fails due to a client-side error.
        Expected outcome: An exception is raised indicating the upload failure.
        """
        s3_client_mock.upload_fileobj.side_effect = ClientError({'Error': {'Code': '500', 'Message': 'Internal Error'}}, 'Upload')
        with pytest.raises(Exception, match="Failed to upload file."):
            s3_service.upload_file_to_s3(mock_file)
    def test_list_files_in_s3_success(self, s3_service: S3Service, s3_client_mock: MagicMock) -> None:
        """Tests successful retrieval of files from S3.
        Scenario: There are files in the S3 bucket.
        Expected outcome: The function returns a list of file names.
        """
        s3_client_mock.list_objects_v2.return_value = {
            'Contents': [{'Key': 'file1.txt'}, {'Key': 'file2.txt'}]
        }
        files = s3_service.list_files_in_s3()
        assert files == ['file1.txt', 'file2.txt']
        s3_client_mock.list_objects_v2.assert_called_once_with(Bucket='test-bucket')
    def test_list_files_in_s3_no_files(self, s3_service: S3Service, s3_client_mock: MagicMock) -> None:
        """Tests the case where no files exist in S3.
        Scenario: The S3 bucket is empty.
        Expected outcome: An empty list is returned.
        """
        s3_client_mock.list_objects_v2.return_value = {}
        files = s3_service.list_files_in_s3()
        assert files == []
        s3_client_mock.list_objects_v2.assert_called_once_with(Bucket='test-bucket')
    def test_list_files_in_s3_client_error(self, s3_service: S3Service, s3_client_mock: MagicMock) -> None:
        """Tests list failure due to a ClientError.
        Scenario: Listing files fails due to a client-side error.
        Expected outcome: An exception is raised indicating the failure.
        """
        s3_client_mock.list_objects_v2.side_effect = ClientError({'Error': {'Code': '500', 'Message': 'Internal Error'}}, 'List')
        with pytest.raises(Exception, match="Failed to list files."):
            s3_service.list_files_in_s3()
    def test_get_file_from_s3_success(self, s3_service: S3Service, s3_client_mock: MagicMock) -> None:
        """Tests successful retrieval of a file from S3.
        Scenario: A valid file name is provided, and the file exists.
        Expected outcome: The function returns the file content.
        """
        mock_body = MagicMock()  # Simulates the StreamingBody
        s3_client_mock.get_object.return_value = {'Body': mock_body}
        body = s3_service.get_file_from_s3('test_file.txt')
        assert body == mock_body
        s3_client_mock.get_object.assert_called_once_with(Bucket='test-bucket', Key='test_file.txt')
    def test_get_file_from_s3_file_not_found(self, s3_service: S3Service, s3_client_mock: MagicMock) -> None:
        """Tests retrieval failure when the file does not exist.
        Scenario: The specified file does not exist in the S3 bucket.
        Expected outcome: A FileNotFoundError is raised.
        """
        s3_client_mock.get_object.side_effect = s3_client_mock.exceptions.NoSuchKey
        with pytest.raises(FileNotFoundError, match="File test_file.txt not found."):
            s3_service.get_file_from_s3('test_file.txt')
    def test_get_file_from_s3_client_error(self, s3_service: S3Service, s3_client_mock: MagicMock) -> None:
        """Tests retrieval failure due to a ClientError.
        Scenario: A client-side error occurs while retrieving the file.
        Expected outcome: An exception is raised indicating the retrieval failure.
        """
        s3_client_mock.get_object.side_effect = ClientError({'Error': {'Code': '500', 'Message': 'Internal Error'}}, 'Get')
        with pytest.raises(Exception, match="Failed to retrieve file."):
            s3_service.get_file_from_s3('test_file.txt')
