import boto3
from botocore.exceptions import NoCredentialsError, ClientError


def create_s3_client():
    """
    Create an S3 client using the default AWS credentials.

    :return: S3 client
    """
    try:
        return boto3.client('s3')
    except NoCredentialsError:
        raise Exception("AWS credentials not found.")


def handle_s3_exception(e: ClientError):
    """
    Handle exceptions raised by the S3 client.

    :param e: ClientError exception
    :return: None
    """
    error_code = e.response['Error']['Code']
    if error_code == 'NoSuchBucket':
        raise Exception("The specified bucket does not exist.")
    elif error_code == 'NoSuchKey':
        raise Exception("The specified key does not exist.")
    else:
        raise Exception(f"An error occurred: {e}")

# TODO: Add more utility functions as needed for S3 operations.