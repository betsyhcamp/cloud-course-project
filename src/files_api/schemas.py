from datetime import datetime
from typing import (
    List,
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
)

DEFAULT_GET_FILES_PAGE_SIZE = 10
DEFAULT_GET_FILES_MIN_PAGE_SIZE = 10
DEFAULT_GET_FILES_MAX_PAGE_SIZE = 100
DEFAULT_GET_FILES_DIRECTORY = ""


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
    page_size: int = Field(
        DEFAULT_GET_FILES_PAGE_SIZE,
        ge=DEFAULT_GET_FILES_MIN_PAGE_SIZE,
        le=DEFAULT_GET_FILES_MAX_PAGE_SIZE,
    )
    directory: Optional[str] = ""
    page_token: Optional[str] = None


# delete
class DeleteFileResponse(BaseModel):
    message: str
