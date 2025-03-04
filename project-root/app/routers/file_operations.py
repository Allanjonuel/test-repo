from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from typing import List
from app.services.s3_service import S3Service
from app.utils.validation import validate_file
from app.utils.error_handling import handle_s3_error
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the router
router = APIRouter()

# Dependency to get S3 service
async def get_s3_service():
    return S3Service()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...), s3_service: S3Service = Depends(get_s3_service)):
    """
    Upload a file to the S3 bucket.

    - **file**: The file to be uploaded.
    """
    try:
        validate_file(file)
        result = await s3_service.upload_file(file)
        logger.info(f"File {file.filename} uploaded successfully.")
        return {"message": "File uploaded successfully", "file_url": result}
    except Exception as e:
        logger.error(f"Error uploading file {file.filename}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/files", response_model=List[str])
async def list_files(s3_service: S3Service = Depends(get_s3_service)):
    """
    List all files in the S3 bucket.
    """
    try:
        files = await s3_service.list_files()
        logger.info("Files listed successfully.")
        return files
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/files/{file_name}")
async def get_file_content(file_name: str, s3_service: S3Service = Depends(get_s3_service)):
    """
    Retrieve the content of a specified file from the S3 bucket.

    - **file_name**: The name of the file to retrieve.
    """
    try:
        content = await s3_service.get_file_content(file_name)
        logger.info(f"File {file_name} retrieved successfully.")
        return content
    except Exception as e:
        logger.error(f"Error retrieving file {file_name}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))