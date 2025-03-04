from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from src.services.s3_service import S3Service
from botocore.exceptions import BotoCoreError, ClientError

router = APIRouter()
s3_service = S3Service()

BUCKET_NAME = "bucket-for-ai-generated-content"


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file to the specified S3 bucket.

    :param file: The file to upload.
    :return: Success message or error message.
    """
    try:
        s3_service.upload_file(BUCKET_NAME, file)
        return JSONResponse(content={"message": "File uploaded successfully."}, status_code=200)
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")


@router.get("/files")
async def list_files():
    """
    List all files in the specified S3 bucket.

    :return: List of file names or error message.
    """
    try:
        files = s3_service.list_files(BUCKET_NAME)
        return JSONResponse(content={"files": files}, status_code=200)
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")


@router.get("/files/{file_name}")
async def get_file_content(file_name: str):
    """
    Retrieve the content of a specified file from the S3 bucket.

    :param file_name: The name of the file to retrieve.
    :return: File content or error message.
    """
    try:
        content = s3_service.get_file_content(BUCKET_NAME, file_name)
        return JSONResponse(content={"content": content}, status_code=200)
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve file content: {str(e)}")