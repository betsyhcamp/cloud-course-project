from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import StreamingResponse

from files_api.s3.delete_objects import delete_s3_object
from files_api.s3.read_objects import (
    fetch_s3_object,
    fetch_s3_objects_metadata,
    fetch_s3_objects_using_page_token,
    object_exists_in_s3,
)
from files_api.s3.write_objects import upload_s3_object
from files_api.schemas import (
    FileMetadata,
    GetFilesQueryParams,
    GetFilesResponse,
    PutFileResponse,
)
from files_api.settings import Settings

##################
# --- Routes --- #
##################

ROUTER = APIRouter(tags=["Files"])


@ROUTER.put(
    "/files/{file_path:path}",
    responses={
        status.HTTP_200_OK: {"model": PutFileResponse},
        status.HTTP_201_CREATED: {"model": PutFileResponse},
    },
)
async def upload_file(
    request: Request,
    file_path: str,
    file_content: UploadFile,
    response: Response,
) -> PutFileResponse:
    """Upload a file."""
    settings: Settings = request.app.state.settings

    file_bytes: bytes = await file_content.read()

    object_already_exists = object_exists_in_s3(bucket_name=settings.s3_bucket_name, object_key=file_path)
    if object_already_exists:
        message = f"Existing file updated at path: /{file_path}"
        response.status_code = status.HTTP_200_OK
    else:
        message = f"New file uploaded at path: /{file_path}"
        response.status_code = status.HTTP_201_CREATED

    upload_s3_object(
        bucket_name=settings.s3_bucket_name,
        object_key=file_path,
        file_content=file_bytes,
        content_type=file_content.content_type,
    )

    return PutFileResponse(
        file_path=file_path,
        message=message,
    )


@ROUTER.get("/files")
async def list_files(
    request: Request,
    query_params: GetFilesQueryParams = Depends(),  # noqa: B008
) -> GetFilesResponse:
    """List files with pagination."""
    settings: Settings = request.app.state.settings
    if query_params.page_token:
        files, next_page_token = fetch_s3_objects_using_page_token(
            bucket_name=settings.s3_bucket_name,
            continuation_token=query_params.page_token,
            max_keys=query_params.page_size,
        )
    else:
        files, next_page_token = fetch_s3_objects_metadata(
            bucket_name=settings.s3_bucket_name,
            prefix=query_params.directory,
            max_keys=query_params.page_size,
        )
    file_metadata_objs = [
        FileMetadata(
            file_path=f"{item['Key']}",
            last_modified=item["LastModified"],
            size_bytes=item["Size"],
        )
        for item in files
    ]

    return GetFilesResponse(files=file_metadata_objs, next_page_token=next_page_token if next_page_token else None)


@ROUTER.head(
    "/files/{file_path:path}",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "File not found for the given `file_path`."},
        status.HTTP_200_OK: {
            "headers": {
                "Content-Type": {
                    "description": "The MIME type",
                    "example": "text/plain",
                    "schema": {"type": "string"},
                },
                "Content-Length": {
                    "description": "The size of the file in bytes.",
                    "example": 64,
                    "schema": {"type": "integer"},
                },
                "Last Modified": {
                    "description": "The last date the file was modified.",
                    "example": "Thu, 01 Jan2024 00:00:00 GMT",
                    "schema": {"type": "string", "format": "date-time"},
                },
            },
        },
    },
)
async def get_file_metadata(request: Request, file_path: str, response: Response) -> Response:
    """Retrieve file metadata.

    Note: by convention, HEAD requests MUST NOT return a body in the response.
    """
    settings: Settings = request.app.state.settings

    # before trying to retrieve object metadata, make sure object exists
    object_exists = object_exists_in_s3(bucket_name=settings.s3_bucket_name, object_key=file_path)
    if not object_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    get_object_response = fetch_s3_object(
        bucket_name=settings.s3_bucket_name,
        object_key=file_path,
    )
    response.headers["Content-Type"] = get_object_response["ContentType"]
    response.headers["Content-Length"] = str(get_object_response["ContentLength"])
    response.headers["Last-Modified"] = get_object_response["LastModified"].strftime("%a, %d %b %Y %H:%M:%S GMT")
    response.status_code = status.HTTP_200_OK
    return response


@ROUTER.get(
    "/files/{file_path:path}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "File not found for the given `file_path`.",
        },
        status.HTTP_200_OK: {
            "description": "The file content.",
            "content": {
                "application/octet-stream": {
                    "schema": {"type": "string", "format": "binary"},
                },
            },
        },
    },
)
async def get_file(
    request: Request,
    file_path: str,
) -> StreamingResponse:
    """Retrieve a file."""

    # 1 -Business logic: Error that the user can fix
    # error case: object does not exist in the bucket
    # error case: invalid inputs

    # 2 - Internal Server Error - errors that the user cannot fix
    # error case: not authenticated/authorized to make calls to cloud service provider
    # error case: the bucket does not exist

    settings: Settings = request.app.state.settings

    object_exists = object_exists_in_s3(bucket_name=settings.s3_bucket_name, object_key=file_path)
    if not object_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    get_object_response = fetch_s3_object(bucket_name=settings.s3_bucket_name, object_key=file_path)

    return StreamingResponse(
        content=get_object_response["Body"],
        media_type=get_object_response["ContentType"],
    )


@ROUTER.delete(
    "/files/{file_path:path}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "File not found for the given `file_path`.",
        },
        status.HTTP_204_NO_CONTENT: {
            "description": "File deleted successfully.",
        },
    },
)
async def delete_file(
    request: Request,
    file_path: str,
    response: Response,
) -> Response:
    """
    Delete a file.

    NOTE: DELETE requests MUST NOT return a body in the response.
    """
    settings: Settings = request.app.state.settings

    # before deleting object, make sure it exists
    object_exists = object_exists_in_s3(bucket_name=settings.s3_bucket_name, object_key=file_path)
    if not object_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    # delete object, if it extists
    delete_s3_object(bucket_name=settings.s3_bucket_name, object_key=file_path)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response
