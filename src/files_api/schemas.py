from datetime import datetime
from typing import (
    List,
    Optional,
)

from pydantic import BaseModel


####################################
# --- Request/response schemas --- #
####################################


# create/update
class PutFileResponse(BaseModel):
    file_path: str
    message: str


# read
class FileMetadata(BaseModel):
    file_path: str
    last_modified: datetime
    size_bytes: int


# read
class GetFilesResponse(BaseModel):
    files: List[FileMetadata]
    next_page_token: Optional[str]


# read
class GetFilesQueryParams(BaseModel):
    page_size: int = 10
    directory: Optional[str] = ""
    page_token: Optional[str] = None


# delete
class DeleteFileResponse(BaseModel):
    message: str
