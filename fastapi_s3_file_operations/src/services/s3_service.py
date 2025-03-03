import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import HTTPException


class S3Service:
    def __init__(self, bucket_name: str = "bucket-for-ai-generated-content"):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name

    def upload_file(self, file) -> str:
        """
        Upload a file to the S3 bucket.

        :param file: File to be uploaded
        :return: URL of the uploaded file
        """
        try:
            self.s3_client.upload_fileobj(file.file, self.bucket_name, file.filename)
            file_url = f"https://{self.bucket_name}.s3.amazonaws.com/{file.filename}"
            return file_url
        except NoCredentialsError:
            raise HTTPException(status_code=403, detail="AWS credentials not found.")
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload file: {e}")

    def list_files(self) -> list:
        """
        List all files in the S3 bucket.

        :return: List of file names
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                return [item['Key'] for item in response['Contents']]
            return []
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Failed to list files: {e}")

    def get_file_content(self, file_name: str) -> str:
        """
        Retrieve the content of a specified file from the S3 bucket.

        :param file_name: Name of the file to retrieve
        :return: Content of the file
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_name)
            content = response['Body'].read().decode('utf-8')
            return content
        except self.s3_client.exceptions.NoSuchKey:
            raise HTTPException(status_code=404, detail="File not found.")
        except ClientError as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve file content: {e}")
