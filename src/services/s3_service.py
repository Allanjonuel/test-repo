import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from typing import List


class S3Service:
    def __init__(self, bucket_name: str = "bucket-for-ai-generated-content"):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name

    def upload_file(self, file) -> str:
        """
        Upload a file to the S3 bucket.

        :param file: The file to be uploaded.
        :return: The URL of the uploaded file.
        """
        try:
            self.s3_client.upload_fileobj(file.file, self.bucket_name, file.filename)
            file_url = f"https://{self.bucket_name}.s3.amazonaws.com/{file.filename}"
            return file_url
        except NoCredentialsError:
            raise Exception("Credentials not available")
        except ClientError as e:
            raise Exception(e)

    def list_files(self) -> List[str]:
        """
        List all files in the S3 bucket.

        :return: A list of file names.
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                return [item['Key'] for item in response['Contents']]
            else:
                return []
        except ClientError as e:
            raise Exception(e)

    def get_file_content(self, file_name: str) -> str:
        """
        Retrieve the content of a specified file from the S3 bucket.

        :param file_name: The name of the file to retrieve.
        :return: The content of the file as a string.
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_name)
            return response['Body'].read().decode('utf-8')
        except ClientError as e:
            raise Exception(e)
