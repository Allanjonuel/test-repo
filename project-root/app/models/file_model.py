from pydantic import BaseModel
from typing import List

class FileUploadResponse(BaseModel):
    message: str
    file_url: str

class FileListResponse(BaseModel):
    files: List[str]