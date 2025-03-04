from pydantic import BaseModel
from typing import Optional

class FileUploadResponse(BaseModel):
    file_url: str
    message: Optional[str] = "File uploaded successfully."

class FileListResponse(BaseModel):
    files: list[str]

class FileContentResponse(BaseModel):
    file_content: str
    message: Optional[str] = "File content retrieved successfully."