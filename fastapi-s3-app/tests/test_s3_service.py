import unittest
from unittest.mock import patch, MagicMock
from app.services.s3_service import S3Service
from botocore.exceptions import NoCredentialsError, ClientError

class TestS3Service(unittest.TestCase):
    def setUp(self):
        self.s3_service = S3Service()

    @patch('boto3.client')
    def test_upload_file_to_s3_success(self, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_file = MagicMock()
        mock_file.filename = 'test.txt'

        file_url = self.s3_service.upload_file_to_s3(mock_file)

        mock_s3_client.upload_fileobj.assert_called_once_with(mock_file.file, 'bucket-for-ai-generated-content', 'test.txt')
        self.assertEqual(file_url, 'https://bucket-for-ai-generated-content.s3.amazonaws.com/test.txt')

    @patch('boto3.client')
    def test_upload_file_to_s3_no_credentials(self, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.upload_fileobj.side_effect = NoCredentialsError
        mock_file = MagicMock()

        with self.assertRaises(Exception) as context:
            self.s3_service.upload_file_to_s3(mock_file)

        self.assertEqual(str(context.exception), 'AWS credentials not available.')

    @patch('boto3.client')
    def test_list_files_in_s3_success(self, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.list_objects_v2.return_value = {
            'Contents': [{'Key': 'file1.txt'}, {'Key': 'file2.txt'}]
        }

        files = self.s3_service.list_files_in_s3()

        mock_s3_client.list_objects_v2.assert_called_once_with(Bucket='bucket-for-ai-generated-content')
        self.assertEqual(files, ['file1.txt', 'file2.txt'])

    @patch('boto3.client')
    def test_list_files_in_s3_no_contents(self, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.list_objects_v2.return_value = {}

        files = self.s3_service.list_files_in_s3()

        self.assertEqual(files, [])

    @patch('boto3.client')
    def test_get_file_from_s3_success(self, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_response = {'Body': MagicMock()}
        mock_s3_client.get_object.return_value = mock_response

        file_content = self.s3_service.get_file_from_s3('test.txt')

        mock_s3_client.get_object.assert_called_once_with(Bucket='bucket-for-ai-generated-content', Key='test.txt')
        self.assertEqual(file_content, mock_response['Body'])

    @patch('boto3.client')
    def test_get_file_from_s3_file_not_found(self, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.get_object.side_effect = mock_s3_client.exceptions.NoSuchKey

        with self.assertRaises(FileNotFoundError):
            self.s3_service.get_file_from_s3('nonexistent.txt')

if __name__ == '__main__':
    unittest.main()
