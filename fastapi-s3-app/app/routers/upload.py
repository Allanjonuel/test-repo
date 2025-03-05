from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.s3_service import S3Service
from app.utils.validation import validate_file_type, validate_file_size
import logging

router = APIRouter()

# Initialize S3 service
s3_service = S3Service()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file to the S3 bucket.

    Args:
        file (UploadFile): The file to be uploaded.

    Returns:
        JSONResponse: A response indicating the success or failure of the upload.
    """
    try:
        # Validate file type and size
        validate_file_type(file)
        validate_file_size(file)

        # Upload file to S3
        file_url = s3_service.upload_file_to_s3(file)

        logger.info(f"File {file.filename} uploaded successfully.")
        return JSONResponse(status_code=200, content={"message": "File uploaded successfully", "file_url": file_url})
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# TODO: Implement rate limiting to prevent abuse of the upload endpoint
# TODO: Add more specific error handling for different exceptions