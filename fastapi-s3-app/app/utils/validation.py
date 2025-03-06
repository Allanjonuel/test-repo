from fastapi import UploadFile, HTTPException

# Define allowed file types and maximum file size (e.g., 5 MB)
ALLOWED_FILE_TYPES = {"image/jpeg", "image/png", "application/pdf"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_file_type(file: UploadFile):
    """
    Validate the file type of the uploaded file.

    Args:
        file (UploadFile): The file to be validated.

    Raises:
        HTTPException: If the file type is not allowed.
    """
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type.")


def validate_file_size(file: UploadFile):
    """
    Validate the file size of the uploaded file.

    Args:
        file (UploadFile): The file to be validated.

    Raises:
        HTTPException: If the file size exceeds the maximum limit.
    """
    file.file.seek(0, 2)  # Move the cursor to the end of the file
    file_size = file.file.tell()
    file.file.seek(0)  # Reset the cursor to the beginning of the file

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the maximum limit of 5 MB.")

# TODO: Add more validation functions if needed, such as checking for specific file content or structure