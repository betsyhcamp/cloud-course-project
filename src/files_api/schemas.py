from datetime import datetime
from typing import (
    List,
    Optional,
)

from pydantic import (
    BaseModel,
    ConfigDict,
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
    """Response model for `PUT /files/:file_path`."""

    file_path: str = Field(
        description="The path of the file.",
        json_schema_extra={"example": "path/to/file_example.txt"},
    )
    message: str = Field(description="A message about the operation.")


# read
class FileMetadata(BaseModel):
    """Metadata of a file."""

    file_path: str = Field(
        description="The path of the file.", json_schema_extra={"example": "path/to/file_example.txt"}
    )
    last_modified: datetime = Field(description="The most recent timestamp the file was modified.")
    size_bytes: int = Field(description="The size of the file in bytes.")


# read
class GetFilesResponse(BaseModel):
    """Response model for `GET /files`."""

    files: List[FileMetadata]
    next_page_token: Optional[str]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "files": [
                    {
                        "file_path": "path/to/file_example.txt",
                        "last_modified": "2022-01-01T00:00:00Z",
                        "size_bytes": 125,
                    }
                ],
                "next_page_token": "next_page_token_example",
            }
        }
    )


# read
class GetFilesQueryParams(BaseModel):
    """Query parameters for `GET /files`."""

    page_size: int = Field(
        DEFAULT_GET_FILES_PAGE_SIZE,
        ge=DEFAULT_GET_FILES_MIN_PAGE_SIZE,
        le=DEFAULT_GET_FILES_MAX_PAGE_SIZE,
    )
    directory: Optional[str] = Field(DEFAULT_GET_FILES_DIRECTORY, description="The directory to list files from.")
    page_token: Optional[str] = Field(None, description="The token for the next page.")


# delete
class DeleteFileResponse(BaseModel):
    """Response model for `DELETE /files/:file_path`."""

    message: str = Field(description="A message about the operation.")
