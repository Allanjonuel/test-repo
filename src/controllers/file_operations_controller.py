from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from src.services.s3_service import S3Service

router = APIRouter()

# Initialize the S3 service
s3_service = S3Service()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a file to the S3 bucket.
    
    :param file: The file to be uploaded.
    :return: JSON response with the status of the upload.
    """
    try:
        result = s3_service.upload_file(file)
        return JSONResponse(content={"message": "File uploaded successfully", "file_url": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files")
async def list_files():
    """
    Endpoint to list all files in the S3 bucket.
    
    :return: JSON response with the list of files.
    """
    try:
        files = s3_service.list_files()
        return JSONResponse(content={"files": files})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files/{file_name}")
async def get_file_content(file_name: str):
    """
    Endpoint to retrieve the content of a specified file from the S3 bucket.
    
    :param file_name: The name of the file to retrieve.
    :return: JSON response with the content of the file.
    """
    try:
        content = s3_service.get_file_content(file_name)
        return JSONResponse(content={"file_name": file_name, "content": content})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
