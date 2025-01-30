"""Test cases for `s3.delete_objects`"""

import boto3
from moto import mock_aws

from files_api.s3.delete_objects import delete_s3_object
from files_api.s3.read_objects import object_exists_in_s3
from files_api.s3.write_objects import upload_s3_object
from tests.consts import TEST_BUCKET_NAME


@mock_aws
# pylint: disable=unused-argument
def test_delete_existing_s3_object(mocked_aws: None):
    s3_client = boto3.client("s3")
    s3_client.put_object(Bucket=TEST_BUCKET_NAME, Key="testfile.txt", Body="test content")
    delete_s3_object(TEST_BUCKET_NAME, "testfile.txt")
    assert not s3_client.list_objects_v2(Bucket=TEST_BUCKET_NAME).get("Contents")


@mock_aws
# pylint: disable=unused-argument
def test_delete_nonexistent_s3_object(mocked_aws: None):
    # create file
    upload_s3_object(bucket_name=TEST_BUCKET_NAME, object_key="testfile.txt", file_content=b"test content")
    # delete the file (so we know itis not present)
    delete_s3_object(bucket_name=TEST_BUCKET_NAME, object_key="testfile.txt")
    # delete the file again
    delete_s3_object(bucket_name=TEST_BUCKET_NAME, object_key="testfile.txt")
    # test whether the file is found
    assert object_exists_in_s3(TEST_BUCKET_NAME, "testfile.txt") is False
