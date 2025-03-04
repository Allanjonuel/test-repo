from fastapi import HTTPException, status
from botocore.exceptions import ClientError
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_s3_error(e: ClientError):
    """
    Handle errors from AWS S3 operations and raise appropriate HTTP exceptions.

    :param e: The ClientError exception from boto3.
    :raises HTTPException: Corresponding HTTP exception based on the error code.
    """
    error_code = e.response['Error']['Code']
    logger.error(f"S3 ClientError: {error_code} - {e.response['Error']['Message']}")

    if error_code == 'NoSuchKey':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
    elif error_code == 'AccessDenied':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to the resource.")
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred with the S3 service.")


def handle_general_error(e: Exception):
    """
    Handle general exceptions and raise an HTTP 500 error.

    :param e: The exception to handle.
    :raises HTTPException: HTTP 500 error indicating an internal server error.
    """
    logger.error(f"Unexpected error: {str(e)}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
