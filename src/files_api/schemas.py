import os
from ast import Str
from datetime import datetime
from typing import (
    List,
    Optional,
)

from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from files_api.s3.delete_objects import delete_s3_object
from files_api.s3.read_objects import (
    fetch_s3_object,
    fetch_s3_objects_metadata,
    fetch_s3_objects_using_page_token,
    object_exists_in_s3,
)

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
