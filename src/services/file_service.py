import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import UploadFile
from typing import List

class FileService:
    def __init__(self):
        # Initialize the S3 client
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'bucket-for-ai-generated-content'

    def upload_file_to_s3(self, file: UploadFile) -> str:
        """
        Upload a file to the specified S3 bucket.

        :param file: UploadFile object
        :return: URL of the uploaded file
        """
        try:
            self.s3_client.upload_fileobj(file.file, self.bucket_name, file.filename)
            file_url = f"https://{self.bucket_name}.s3.amazonaws.com/{file.filename}"
            return file_url
        except NoCredentialsError:
            raise Exception("AWS credentials not found.")
        except ClientError as e:
            raise Exception(f"Failed to upload file: {e}")

    def list_files_in_s3(self) -> List[str]:
        """
        List all files in the specified S3 bucket.

        :return: List of file names
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                return [item['Key'] for item in response['Contents']]
            return []
        except ClientError as e:
            raise Exception(f"Failed to list files: {e}")

    def get_file_content_from_s3(self, file_name: str) -> str:
        """
        Retrieve the content of a specified file from the S3 bucket.

        :param file_name: Name of the file to retrieve
        :return: Content of the file
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_name)
            return response['Body'].read().decode('utf-8')
        except ClientError as e:
            raise Exception(f"Failed to retrieve file content: {e}")
