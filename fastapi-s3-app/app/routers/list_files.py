from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.services.s3_service import S3Service
import logging

router = APIRouter()

# Initialize S3 service
s3_service = S3Service()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/files/")
async def list_files():
    """
    List all files in the S3 bucket.

    Returns:
        JSONResponse: A response containing the list of files or an error message.
    """
    try:
        # List files in S3
        files = s3_service.list_files_in_s3()

        logger.info("Files listed successfully.")
        return JSONResponse(status_code=200, content={"files": files})
    except Exception as e:
        logger.error(f"Failed to list files: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# TODO: Implement pagination for listing files if the number of files is large
# TODO: Add more specific error handling for different exceptions