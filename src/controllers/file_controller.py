from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from src.services.file_service import FileService

router = APIRouter()

# Initialize the file service
file_service = FileService()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a file to the S3 bucket.
    """
    try:
        file_url = file_service.upload_file_to_s3(file)
        return JSONResponse(status_code=200, content={"file_url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files")
async def list_files() -> List[str]:
    """
    Endpoint to list all files in the S3 bucket.
    """
    try:
        files = file_service.list_files_in_s3()
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files/{file_name}")
async def get_file_content(file_name: str):
    """
    Endpoint to retrieve the content of a specified file from the S3 bucket.
    """
    try:
        file_content = file_service.get_file_content_from_s3(file_name)
        return JSONResponse(status_code=200, content={"file_content": file_content})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
