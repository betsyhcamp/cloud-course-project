"""Test cases for `s3.read_objects`."""

import boto3
from moto import mock_aws

from files_api.s3.read_objects import (
    fetch_s3_objects_metadata,
    fetch_s3_objects_using_page_token,
    object_exists_in_s3,
)
from tests.consts import TEST_BUCKET_NAME


@mock_aws
# pylint: disable=unused-argument
def test_object_exists_in_s3(mocked_aws):
    """Assert that `object_exists_in_s3` returns the correct value when an object is or isn't present."""
    s3_client = boto3.client("s3")
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="testfile.txt", Body="test content")
    assert object_exists_in_s3(TEST_BUCKET_NAME, "testfile.txt") is True
    assert object_exists_in_s3(TEST_BUCKET_NAME, "nonexistent.txt") is False


@mock_aws
# pylint: disable=unused-argument
def test_pagination(mocked_aws):  # noqa: R701
    """Asset that pagination works correctly."""

    s3_client = boto3.client("s3")
    # Upload 5 objects
    for object_num in [1, 2, 3, 4, 5]:
        s3_client.put_object(
            Bucket=TEST_BUCKET_NAME,
            Key=f"file_{object_num}.txt",
            Body=f"content {object_num}",
        )

    # paginate 2 files
    files, next_page_token = fetch_s3_objects_metadata(TEST_BUCKET_NAME, max_keys=2)
    assert len(files) == 2
    assert files[0]["Key"] == "file_1.txt"
    assert files[1]["Key"] == "file_2.txt"

    # paginate 2 files
    files, next_page_token = fetch_s3_objects_using_page_token(TEST_BUCKET_NAME, next_page_token, max_keys=2)
    assert len(files) == 2
    assert files[0]["Key"] == "file_3.txt"
    assert files[1]["Key"] == "file_4.txt"

    # paginate remaining files
    files, next_page_token = fetch_s3_objects_using_page_token(TEST_BUCKET_NAME, next_page_token, max_keys=2)
    assert len(files) == 1
    assert files[0]["Key"] == "file_5.txt"
    assert next_page_token is None


@mock_aws
# pylint: disable=unused-argument
def test_mixed_page_sizes(mocked_aws: None):  # noqa: R701 - too complex
    s3_client = boto3.client("s3")
    # upload objects
    for object_num in [1, 2, 3, 4, 5, 6]:
        s3_client.put_object(
            Bucket=TEST_BUCKET_NAME,
            Key=f"file_{object_num}.txt",
            Body=f"content {object_num}",
        )

    # test pagination
    files, next_page_token = fetch_s3_objects_metadata(TEST_BUCKET_NAME, max_keys=3)
    assert len(files) == 3
    assert files[0]["Key"] == "file_1.txt"
    assert files[1]["Key"] == "file_2.txt"
    assert files[2]["Key"] == "file_3.txt"

    files, next_page_token = fetch_s3_objects_using_page_token(TEST_BUCKET_NAME, next_page_token, max_keys=1)
    assert len(files) == 1
    assert files[0]["Key"] == "file_4.txt"

    files, next_page_token = fetch_s3_objects_using_page_token(TEST_BUCKET_NAME, next_page_token, max_keys=3)
    assert len(files) == 2
    assert files[0]["Key"] == "file_5.txt"
    assert files[1]["Key"] == "file_6.txt"
    assert next_page_token is None


@mock_aws
# pylint: disable=unused-argument
def test_directory_queries(mocked_aws: None):  # noqa: R701 - too complex
    """Assert that queries with prefixes work correctly with variety of directory prefixes on object keys."""
    # upload objects with nested paths
    s3_client = boto3.client("s3")
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="dir1/file1.txt", Body="content 1")
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="dir1/file2.txt", Body="content 2")
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="dir2/file3.txt", Body="content 3")
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="dir2/subdir1/file4.txt", Body="content 4")
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="file5.txt", Body="content 5")

    files, next_page_token = fetch_s3_objects_metadata(TEST_BUCKET_NAME, prefix="dir1/")
    assert len(files) == 2
    assert files[0]["Key"] == "dir1/file1.txt"
    assert files[1]["Key"] == "dir1/file2.txt"
    assert next_page_token is None

    files, next_page_token = fetch_s3_objects_metadata(TEST_BUCKET_NAME, prefix="dir2/subdir1/")
    assert len(files) == 1
    assert files[0]["Key"] == "dir2/subdir1/file4.txt"
    assert next_page_token is None

    files, next_page_token = fetch_s3_objects_metadata(TEST_BUCKET_NAME)
    assert len(files) == 5
    assert files[0]["Key"] == "dir1/file1.txt"
    assert files[1]["Key"] == "dir1/file2.txt"
    assert files[2]["Key"] == "dir2/file3.txt"
    assert files[3]["Key"] == "dir2/subdir1/file4.txt"
    assert files[4]["Key"] == "file5.txt"
    assert next_page_token is None
