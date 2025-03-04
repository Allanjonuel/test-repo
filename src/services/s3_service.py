import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import UploadFile
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class S3Service:
    def __init__(self):
        """
        Initialize the S3 client using default AWS credentials.
        """
        self.s3_client = boto3.client('s3')

    def upload_file(self, bucket_name: str, file: UploadFile):
        """
        Upload a file to the specified S3 bucket.

        :param bucket_name: The name of the S3 bucket.
        :param file: The file to upload.
        """
        try:
            logger.info(f"Uploading file {file.filename} to bucket {bucket_name}.")
            self.s3_client.upload_fileobj(file.file, bucket_name, file.filename)
            logger.info("File uploaded successfully.")
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Error uploading file: {str(e)}")
            raise

    def list_files(self, bucket_name: str) -> List[str]:
        """
        List all files in the specified S3 bucket.

        :param bucket_name: The name of the S3 bucket.
        :return: A list of file names.
        """
        try:
            logger.info(f"Listing files in bucket {bucket_name}.")
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            files = [item['Key'] for item in response.get('Contents', [])]
            logger.info(f"Files found: {files}")
            return files
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Error listing files: {str(e)}")
            raise

    def get_file_content(self, bucket_name: str, file_name: str) -> str:
        """
        Retrieve the content of a specified file from the S3 bucket.

        :param bucket_name: The name of the S3 bucket.
        :param file_name: The name of the file to retrieve.
        :return: The content of the file as a string.
        """
        try:
            logger.info(f"Retrieving file {file_name} from bucket {bucket_name}.")
            response = self.s3_client.get_object(Bucket=bucket_name, Key=file_name)
            content = response['Body'].read().decode('utf-8')
            logger.info("File content retrieved successfully.")
            return content
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Error retrieving file content: {str(e)}")
            raise