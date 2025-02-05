"""Pytest fixture to mock AWS services."""

import os
from typing import Generator

import boto3
import botocore
import botocore.exceptions
import pytest
from moto import mock_aws

from tests.consts import TEST_BUCKET_NAME  # all s3 week1 (prior to happy path) tests worked with this
from tests.utils import delete_s3_bucket

# from files_api.main import S3_BUCKET_NAME as TEST_BUCKET_NAME  # used for week2 happy path endpoints


# Set the environment variables to point away from AWS
def point_away_from_aws() -> None:
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


# Our fixture is a function and we have named it as a noun instead
# of verb, because it is a resource that is being provided to the test.


@pytest.fixture(scope="function")
def mocked_aws() -> Generator[None, None, None]:
    """
    Set up a mocked AWS environment for testing and clean up after the test.
    """
    with mock_aws():
        # Set the environment variables to point away from AWS
        point_away_from_aws()

        # 1. Create an S3 bucket
        s3_client = boto3.client("s3")
        s3_client.create_bucket(Bucket=TEST_BUCKET_NAME)

        yield

        # 4. Clean up/Teardown by deleting the bucket
        try:
            delete_s3_bucket(bucket_name=TEST_BUCKET_NAME)
        except botocore.exceptions.ClientError as err:
            if err.response["Error"]["Code"] == "NoSuchBucket":
                pass
            else:
                raise
