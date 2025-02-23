from fastapi import status
from fastapi.testclient import TestClient

from files_api.schemas import GeneratedFileType

# Constants for testing
TEST_FILE_PATH = "test.txt"
TEST_FILE_CONTENT = b"Hello, world!"
TEST_FILE_CONTENT_TYPE = "text/plain"


def test_upload_file_successful_request(client: TestClient):
    # create a file
    # test_file_path = "some/nested/file.txt"
    # test_file_content = b"some content"
    # test_file_content_type = "text/plain"

    response = client.put(
        f"/files/{TEST_FILE_PATH }",
        files={"file_content": (TEST_FILE_PATH, TEST_FILE_CONTENT, TEST_FILE_CONTENT_TYPE)},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "file_path": TEST_FILE_PATH,
        "message": f"New file uploaded at path: /{TEST_FILE_PATH}",
    }

    # update and existing file
    updated_content = b"updated_content"
    response = client.put(
        f"/files/{TEST_FILE_PATH}",
        files={"file_content": (TEST_FILE_PATH, updated_content, TEST_FILE_CONTENT_TYPE)},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "file_path": TEST_FILE_PATH,
        "message": f"Existing file updated at path: /{TEST_FILE_PATH}",
    }


def test_list_files_with_pagination(client: TestClient):
    # Upload files
    for i in range(15):
        client.put(
            f"/files/file{i}.txt",
            files={"file_content": (f"file{i}.txt", TEST_FILE_CONTENT, TEST_FILE_CONTENT_TYPE)},
        )
    # List files with page size 10
    response = client.get("/files?page_size=10")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["files"]) == 10
    assert "next_page_token" in data


def test_get_file_metadata(client: TestClient):
    # upload file
    client.put(
        f"/files/{TEST_FILE_PATH}",
        files={"file_content": (TEST_FILE_PATH, TEST_FILE_CONTENT, TEST_FILE_CONTENT_TYPE)},
    )

    # get metadata of file
    response = client.head(f"/files/{TEST_FILE_PATH}")
    assert response.status_code == status.HTTP_200_OK
    headers = response.headers
    assert headers["Content-Type"] == TEST_FILE_CONTENT_TYPE
    assert headers["Content-Length"] == str(len(TEST_FILE_CONTENT))
    assert "Last-Modified" in headers


def test_get_file(client: TestClient):
    # upload file
    client.put(
        f"/files/{TEST_FILE_PATH}",
        files={"file_content": (TEST_FILE_PATH, TEST_FILE_CONTENT, TEST_FILE_CONTENT_TYPE)},
    )

    # get file
    response = client.get(f"/files/{TEST_FILE_PATH}")
    assert response.status_code == status.HTTP_200_OK
    assert response.content == TEST_FILE_CONTENT


def test_delete_file(client: TestClient):
    # upload file
    client.put(
        f"/files/{TEST_FILE_PATH}",
        files={"file_content": (TEST_FILE_PATH, TEST_FILE_CONTENT, TEST_FILE_CONTENT_TYPE)},
    )

    # delete file
    response = client.delete(f"/files/{TEST_FILE_PATH}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(f"/files/{TEST_FILE_PATH}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_generate_image(client: TestClient):
    """Test generating image using POST method."""
    IMAGE_FILE_PATH = "some/nested/path/image.png"  # pylint: disable=invalid-name
    response = client.post(
        url=f"/v1/files/generated/{IMAGE_FILE_PATH}",
        params={"prompt": "Test Prompt", "file_type": GeneratedFileType.IMAGE.value},
    )

    respone_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert (
        respone_data["message"]
        == f"New {GeneratedFileType.IMAGE.value} file generated and uploaded at path: {IMAGE_FILE_PATH}"
    )

    # Get the generated file
    response = client.get(f"/files/{IMAGE_FILE_PATH}")
    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None
    assert response.headers["Content-Type"] == "image/png"
