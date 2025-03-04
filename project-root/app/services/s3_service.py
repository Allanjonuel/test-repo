import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, status
import logging
from typing import List

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self, bucket_name: str = "bucket-for-ai-generated-content"):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name

    async def upload_file(self, file) -> str:
        """
        Upload a file to the S3 bucket.

        :param file: The file to be uploaded.
        :return: The URL of the uploaded file.
        """
        try:
            self.s3_client.upload_fileobj(file.file, self.bucket_name, file.filename)
            file_url = f"https://{self.bucket_name}.s3.amazonaws.com/{file.filename}"
            return file_url
        except ClientError as e:
            logger.error(f"ClientError: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload file.")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")

    async def list_files(self) -> List[str]:
        """
        List all files in the S3 bucket.

        :return: A list of filenames.
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                return [item['Key'] for item in response['Contents']]
            return []
        except ClientError as e:
            logger.error(f"ClientError: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to list files.")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")

    async def get_file_content(self, file_name: str) -> bytes:
        """
        Retrieve the content of a specified file from the S3 bucket.

        :param file_name: The name of the file to retrieve.
        :return: The content of the file.
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_name)
            return response['Body'].read()
        except ClientError as e:
            logger.error(f"ClientError: {str(e)}")
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve file content.")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")