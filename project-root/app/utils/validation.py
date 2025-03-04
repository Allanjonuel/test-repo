from fastapi import HTTPException, UploadFile, status
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define allowed file types and size limit
ALLOWED_FILE_TYPES = {"image/jpeg", "image/png", "application/pdf"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_file(file: UploadFile):
    """
    Validate the uploaded file for type and size constraints.

    :param file: The file to be validated.
    :raises HTTPException: If the file does not meet the validation criteria.
    """
    # Validate file type
    if file.content_type not in ALLOWED_FILE_TYPES:
        logger.error(f"Invalid file type: {file.content_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Allowed types are: JPEG, PNG, PDF."
        )

    # Validate file size
    file_size = _get_file_size(file)
    if file_size > MAX_FILE_SIZE:
        logger.error(f"File size exceeds limit: {file_size} bytes")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the 5 MB limit."
        )

    logger.info(f"File {file.filename} passed validation.")


def _get_file_size(file: UploadFile) -> int:
    """
    Get the size of the uploaded file.

    :param file: The file whose size is to be determined.
    :return: The size of the file in bytes.
    """
    file.file.seek(0, 2)  # Move the cursor to the end of the file
    size = file.file.tell()
    file.file.seek(0)  # Reset the cursor to the beginning of the file
    return size
