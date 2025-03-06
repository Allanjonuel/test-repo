from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.services.s3_service import S3Service
import logging

router = APIRouter()

# Initialize S3 service
s3_service = S3Service()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/files/{file_name}")
async def get_file(file_name: str):
    """
    Retrieve the content of a specified file from the S3 bucket.

    Args:
        file_name (str): The name of the file to retrieve.

    Returns:
        StreamingResponse: A response streaming the file content or an error message.
    """
    try:
        # Retrieve file from S3
        file_content = s3_service.get_file_from_s3(file_name)

        logger.info(f"File {file_name} retrieved successfully.")
        return StreamingResponse(file_content, media_type="application/octet-stream")
    except FileNotFoundError:
        logger.error(f"File {file_name} not found.")
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        logger.error(f"Failed to retrieve file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# TODO: Add more specific error handling for different exceptions
# TODO: Implement rate limiting to prevent abuse of the get file endpoint