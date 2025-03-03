from pydantic import BaseModel

class FileUploadResponse(BaseModel):
    message: str
    file_url: str

class FileListResponse(BaseModel):
    files: list

class FileContentResponse(BaseModel):
    file_name: str
    content: str
