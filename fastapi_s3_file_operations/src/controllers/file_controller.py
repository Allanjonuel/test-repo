from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from src.services.s3_service import S3Service
from src.utils.helpers import handle_error

router = APIRouter()

# Initialize S3 service
s3_service = S3Service()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file to the S3 bucket.

    :param file: File to be uploaded
    :return: JSON response with the status of the upload
    """
    try:
        result = s3_service.upload_file(file)
        return JSONResponse(status_code=200, content={"message": "File uploaded successfully", "file_url": result})
    except Exception as e:
        return handle_error(e)


@router.get("/files")
async def list_files():
    """
    List all files in the S3 bucket.

    :return: JSON response with the list of files
    """
    try:
        files = s3_service.list_files()
        return JSONResponse(status_code=200, content={"files": files})
    except Exception as e:
        return handle_error(e)


@router.get("/files/{file_name}")
async def get_file_content(file_name: str):
    """
    Retrieve the content of a specified file from the S3 bucket.

    :param file_name: Name of the file to retrieve
    :return: JSON response with the file content
    """
    try:
        content = s3_service.get_file_content(file_name)
        return JSONResponse(status_code=200, content={"file_name": file_name, "content": content})
    except Exception as e:
        return handle_error(e)
