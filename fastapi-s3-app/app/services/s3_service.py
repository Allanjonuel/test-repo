import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self, bucket_name: str = "bucket-for-ai-generated-content"):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name

    def upload_file_to_s3(self, file) -> str:
        """
        Upload a file to the S3 bucket.

        Args:
            file: The file to be uploaded.

        Returns:
            str: The URL of the uploaded file.

        Raises:
            Exception: If the upload fails.
        """
        try:
            self.s3_client.upload_fileobj(file.file, self.bucket_name, file.filename)
            file_url = f"https://{self.bucket_name}.s3.amazonaws.com/{file.filename}"
            return file_url
        except NoCredentialsError:
            logger.error("AWS credentials not available.")
            raise Exception("AWS credentials not available.")
        except ClientError as e:
            logger.error(f"Failed to upload file: {e}")
            raise Exception("Failed to upload file.")

    def list_files_in_s3(self) -> List[str]:
        """
        List all files in the S3 bucket.

        Returns:
            List[str]: A list of filenames in the bucket.

        Raises:
            Exception: If listing files fails.
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                return [item['Key'] for item in response['Contents']]
            else:
                return []
        except ClientError as e:
            logger.error(f"Failed to list files: {e}")
            raise Exception("Failed to list files.")

    def get_file_from_s3(self, file_name: str):
        """
        Retrieve a file from the S3 bucket.

        Args:
            file_name (str): The name of the file to retrieve.

        Returns:
            StreamingBody: The content of the file.

        Raises:
            FileNotFoundError: If the file does not exist.
            Exception: If retrieving the file fails.
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_name)
            return response['Body']
        except self.s3_client.exceptions.NoSuchKey:
            logger.error(f"File {file_name} not found.")
            raise FileNotFoundError(f"File {file_name} not found.")
        except ClientError as e:
            logger.error(f"Failed to retrieve file: {e}")
            raise Exception("Failed to retrieve file.")

# TODO: Implement additional methods for deleting files or other S3 operations if needed
# TODO: Add more specific error handling for different exceptions