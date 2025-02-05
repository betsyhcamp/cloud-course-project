import boto3
from fastapi import status
from fastapi.testclient import TestClient

from tests.consts import TEST_BUCKET_NAME
from tests.utils import delete_s3_bucket

NONEXISTANT_FILENAME = "nonexistent_file.txt"


def test_get_nonexistant_file(client: TestClient):
    response = client.get(f"/files/{NONEXISTANT_FILENAME}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "File not found"}


def test_head_nonexistant_file(client: TestClient):
    response = client.head(f"/files/{NONEXISTANT_FILENAME}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistant_file(client: TestClient):
    response = client.delete(f"/files/{NONEXISTANT_FILENAME}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "File not found"}


def test_get_files_invalid_page_size(client: TestClient):
    response = client.get("/files?page_size=-1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = client.get("/files?page_size=101")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_unforseen_500_error(client: TestClient):
    # delete s3 bucket and all objects
    delete_s3_bucket(bucket_name=TEST_BUCKET_NAME)

    # make request to API route that interacts with s3 bucket
    response = client.get("/files")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Internal server error"}
