# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %% [markdown]
# # AWS S3 Operations using Boto3
#
# In this notebook, we will perform several operations on AWS S3 using Boto3.
#
# These operations include:
#
# - creating an S3 bucket
# - writing an object
# - listing objects
# - reading the contents of an object
# - deleting an object
# - updating an object
# - and handling errors for non-existent objects.
#
# We will also demonstrate how to write files with different prefixes and query files by prefix.
#
# ## For this notebook to run...
#
# You will need to have these libraries installed
#
# - `boto3`
# - `boto3-stubs[s3]`
# - `rich`
# - `ipykernel`
#
# The recommended approach is to set up your `pyproject.toml` like so:
#
# ```toml
# [project]
# ...
# dependencies = ['importlib-metadata; python_version<"3.8"', "boto3"]
#
# [project.optional-dependencies]
# stubs = ["boto3-stubs[s3]"]
# notebooks = ["jupyterlab", "ipykernel", "rich"]
# ...
# dev = ["cloud-course-project[test,release,static-code-qa,stubs,notebooks]"]
# ```
#
# So that `pip install --editable './[dev]'` will install all the necessary dependencies into your venv.
#
# ## Instructions for setting up autocompletion in Jupyter Notebooks in VS Code
#
# 1. Install the development dependencies:
# ```sh
# pip install --editable './[dev]'
# ```
# 2. Select the notebook kernel and point it to your virtual environment:
# ```sh
# which python
# ```
# 3. Select the VS Code Python interpreter and point it to your virtual environment:
# ```sh
# which python
# ```
# 4. Reload the VS Code window (`Ctrl/Cmd + Shift + P` > `Developer: Reload Window`)
#

import os
from typing import Optional
from uuid import uuid4  # randomly generated string

# %%
# Import necessary libraries
import boto3
from botocore.exceptions import ClientError
from rich import print  # pretty printing

try:
    from mypy_boto3_s3 import S3Client
except ImportError:
    print("mypy_boto3_s3 not installed")

# %%
# define constants

# Set the profile and region for the AWS SDK (boto3) to use
os.environ["AWS_PROFILE"] = "cloud-course"
os.environ["AWS_REGION"] = "us-west-2"  # Add your region here, like "ap-south-1"

# Access the AWS_REGION variable
aws_region = os.environ.get("AWS_REGION", "us-west-2")
print(f"AWS_REGION: {aws_region}")

# Create a session using the specified profile and region
S3_CLIENT: "S3Client" = boto3.client("s3")

BUCKET_NAME = f"cloud-course-bucket-{str(uuid4())[:4]}"

# Single example object
EXAMPLE_OBJECT_KEY = "example/object/file.txt"
EXAMPLE_OBJECT_CONTENT = "This is a test object."

# Multiple example objects
EXAMPLE_OBJECTS = [
    ("example-a/object/file1.txt", "This is a test object."),
    ("example-a/object/file2.txt", "This is another test object."),
    ("example-a/object/file3.txt", "This is yet another test object."),
    ("example-b/object/file1.txt", "This is a test object."),
    ("example-b/object/file2.txt", "This is another test object."),
    ("example-b/object/file3.txt", "This is yet another test object."),
]

print(f"{BUCKET_NAME=}")
print(f"{EXAMPLE_OBJECT_KEY=}")
print(f"{EXAMPLE_OBJECT_CONTENT=}")

# %% [markdown]
# ## Create a bucket
#
# Here, we create an S3 bucket. Anything you can do in the AWS console, you can do programatically!

# %%
try:
    from mypy_boto3_s3.type_defs import CreateBucketOutputTypeDef
except ImportError:
    print("boto3-stubs[s3] not installed")


def create_bucket(bucket_name: str) -> Optional["CreateBucketOutputTypeDef"]:
    """
    Create an S3 bucket.

    :param bucket_name: Name of the bucket to create
    :type bucket_name: str
    """
    response = S3_CLIENT.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": aws_region},
    )
    return response


# Create the bucket
response = create_bucket(bucket_name=BUCKET_NAME)
print(f"Bucket '{BUCKET_NAME}' created successfully.")
print(response)

# %% [markdown]
# ## Write an object to the bucket
#
# In this exercise, you will write an object to the S3 bucket.
#
# "S3 Paths" are URLs of the form `s3://bucket-name/key`. The `key` is the path to the object in the bucket. For example, `s3://my-bucket-name/my-key` refers to the object with key `my-key` in the bucket `my-bucket-name`.
#
# Some examples:
#
# | Path | Bucket | Object Key |
# | --- | --- | --- |
# | `s3://my-bucket/images/profile.jpeg` | `my-bucket` | `images/profile.jpeg` |
# | `s3://my-bucket/data/2021/01/01/data.csv` | `my-bucket` | `data/2021/01/01/data.csv` |
# | `s3://my-bucket/file.json` | `my-bucket` | `file.json` |
#

# %%
try:
    from mypy_boto3_s3.type_defs import PutObjectOutputTypeDef
except ImportError:
    print("boto3-stubs[s3] not installed")


def write_text_object_to_s3(
    bucket_name: str,
    object_key: str,
    object_content: str,
) -> Optional["PutObjectOutputTypeDef"]:
    """
    Write an object to an S3 bucket.

    :param bucket_name: Name of the bucket to write to
    :param object_key: Key of the object to write
    :param object_content: Content of the object to write
    :return: Response from the put_object call
    """
    response = S3_CLIENT.put_object(Bucket=bucket_name, Key=object_key, Body=object_content)
    return response


# Write the single example to S3
response = write_text_object_to_s3(
    bucket_name=BUCKET_NAME,
    object_key=EXAMPLE_OBJECT_KEY,
    object_content=EXAMPLE_OBJECT_CONTENT,
)
print(response)

# Write the rest of the examples to S3
for object_key, object_content in EXAMPLE_OBJECTS:
    print(f"Writing object to path 's3://{BUCKET_NAME}/{object_key}'")
    write_text_object_to_s3(
        bucket_name=BUCKET_NAME,
        object_key=object_key,
        object_content=object_content,
    )

# %% [markdown]
# ## Read the content of an object
#
# In this exercise, you will read the content of an object from the S3 bucket.

# %%
from botocore.response import StreamingBody


def read_text_object_from_s3(bucket_name: str, object_key: str, verbose: bool = False) -> str | None:
    """
    Read the content of an object from an S3 bucket.

    :param bucket_name: Name of the bucket to read from
    :param object_key: Key of the object to read
    :return: Content of the object
    """
    response = S3_CLIENT.get_object(Bucket=bucket_name, Key=object_key)

    # Note, we need to read the bytestream from the blob and choose how we wish
    # to interpret the bytes. In this case, we interpret them as utf-8 encoded text.
    content_streaming_body: StreamingBody = response["Body"]
    content: str = content_streaming_body.read().decode("utf-8")
    return content


# Read the content of the example object
content = read_text_object_from_s3(BUCKET_NAME, EXAMPLE_OBJECT_KEY)
if content:
    print(f"Content of object '{EXAMPLE_OBJECT_KEY}':\n'{content}'")

# Read the rest of the examples to S3
for object_key, object_content in EXAMPLE_OBJECTS:
    print(f"Reading object in path 's3://{BUCKET_NAME}/{object_key}'")
    content_temp = read_text_object_from_s3(BUCKET_NAME, object_key)
    if content_temp:
        print(f"Content of object '{object_key}':\n'{content}'")
    content_temp = None

# %% [markdown]
# ## Exercise #1 - List objects in the bucket
#
# What if there were more than 1,000 objects in the bucket? How would you list all of them?
#
# Hints
# - Look into ["boto3 paginators"](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html#creating-paginators)
# - OR Look into the [boto3 "resource API"](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/resources.html#resources), a powerful, but potentially less performant, object-oriented way
#   of interacting with AWS resources via boto3
# - OR consider using "Continuation Tokens" with the `list_objects_v2` method.

# %%
try:
    pass
except ImportError:
    print("boto3-stubs[s3] not installed")


def list_all_object_keys_in_bucket(bucket_name: str) -> list[str]:
    """
    List all objects in an S3 bucket.

    :param bucket_name: Name of the bucket to list objects from
    :return: List of object keys
    """

    response = S3_CLIENT.list_objects_v2(Bucket=bucket_name)
    return [content["Key"] for content in response.get("Contents", [])]


# List all objects in the bucket
objects = list_all_object_keys_in_bucket(BUCKET_NAME)
if objects:
    print("Objects in bucket:")
    for obj in objects:
        print(f" - {obj}")

# %% [markdown]
# ## Exercise #2 - Update the object (overwrite with new content)
#
# In this exercise, you will update the content of an existing object in the S3 bucket.

# %%
new_content = "This is updated content."

# the "PUT object" command is an upsert, so it will overwrite existing files
response = write_text_object_to_s3(BUCKET_NAME, EXAMPLE_OBJECT_KEY, new_content)
print(response)

# Read the updated content of the object
updated_content = read_text_object_from_s3(BUCKET_NAME, EXAMPLE_OBJECT_KEY)
if updated_content:
    print(f"Content of updated object '{EXAMPLE_OBJECT_KEY}':\n{updated_content}")

# %% [markdown]
# ## Exercise #3 - Delete the object from the bucket
#
# In this exercise, you will delete an object from the S3 bucket.

# %%
try:
    from mypy_boto3_s3.type_defs import DeleteObjectOutputTypeDef
except ImportError:
    print("boto3-stubs[s3] not installed")


def delete_object_from_s3(
    bucket_name: str,
    object_key: str,
) -> Optional["DeleteObjectOutputTypeDef"]:
    """
    Delete an object from an S3 bucket.

    :param bucket_name: Name of the bucket to delete the object from
    :param object_key: Key of the object to delete
    :return: Response from the delete_object call
    """
    reponse = S3_CLIENT.delete_object(Bucket=bucket_name, Key=object_key)
    return response


# Delete the example object
response = delete_object_from_s3(bucket_name=BUCKET_NAME, object_key=EXAMPLE_OBJECT_KEY)
print(response)

# %% [markdown]
# ## Exercise #4 - Try to read a non-existent object
#
# In this exercise, you will attempt to read a non-existent object from the S3 bucket.
#
# Catch, suppress, and print the `ClientError` exception that is raised when you try to read a non-existent object.

# %%
print(f"Trying to read the deleted object at 's3://{BUCKET_NAME}/{EXAMPLE_OBJECT_KEY}' ...")

delete_object_from_s3(bucket_name=BUCKET_NAME, object_key=EXAMPLE_OBJECT_KEY)

try:
    # try to read the deleted object
    read_text_object_from_s3(BUCKET_NAME, EXAMPLE_OBJECT_KEY)
except ClientError as err:
    assert "NoSuchKey" in str(err)
    print("Error type is ClientError")

# %% [markdown]
# ## Exercise #5 - Try to delete a non-existent object
#
# **Note:** the result of calling `s3_client.delete_object` on a non-existent object is not what you might expect. It succeeds whether or not there exists an object with the given key.
#
# **Note:** The HTTP status code `204` means `No Content`. Or in other words, the request is successful
# but there was nothing to delete.

# %%
non_existant_object_key = EXAMPLE_OBJECT_KEY + "_non_existent"

response = delete_object_from_s3(bucket_name=BUCKET_NAME, object_key=non_existant_object_key)

print(response)

# %% [markdown]
# ## Exercise #6 - Error handling when deleting an object
#
# In this exercise, you will implement error handling to raise a `FileNotFoundError` if you try to delete a non-existent object, i.e., one that has already been deleted or was never written.
#
# Hint, the `s3_client.head_object(...)` method raises an error with status code `404 - File Not Found`
# if no file exists for the given object key.

# %%
HTTP_FILE_NOT_FOUND_ERROR_CODE = "404"


class S3FileNotFoundError(Exception):
    """Raise this exception when an object at a given path is not found in S3."""


def delete_object_or_error_if_not_exists(bucket_name: str, object_key: str) -> None:
    """
    Delete an object from an S3 bucket with error handling for non-existent objects.

    :param bucket_name: Name of the bucket to delete the object from
    :param object_key: Key of the object to delete

    :raises S3FileNotFoundError: if no object exists at the given path
    :raises ClientError: if an unexpected error occurs when using S3 that is not due to file not found
    """
    try:
        S3_CLIENT.head_object(Bucket=bucket_name, Key=object_key)
        delete_object_from_s3(bucket_name=bucket_name, object_key=object_key)
    except ClientError as err:
        is_file_not_found_error = err.response["Error"]["Code"] == HTTP_FILE_NOT_FOUND_ERROR_CODE
        if is_file_not_found_error:
            raise S3FileNotFoundError(f"Object {object_key} DOES NOT exist in bucket {bucket_name}")
        else:
            raise


# Try to delete the non-existent example object with error handling
try:
    delete_object_or_error_if_not_exists(BUCKET_NAME, EXAMPLE_OBJECT_KEY)
except S3FileNotFoundError as err:
    print(err)

# %% [markdown]
# ## Exercise #7 - List objects in the bucket to confirm they were deleted in the previous exercises
#
# In this exercise, you will list all objects in the S3 bucket to confirm that the object has been deleted.

# %%
# List all objects in the bucket
objects = list_all_object_keys_in_bucket(BUCKET_NAME)

if objects:
    print("Objects in bucket:")
    for obj in objects:
        print(f" - {obj}")
else:
    print("Bucket is empty.")


# %% [markdown]
# ## Exercise 8 - List objects by prefix
#
# In this exercise, you will list objects in the S3 bucket by prefix.


# %%
def list_all_objects_in_bucket_by_prefix(bucket_name: str, prefix: str) -> list[str]:
    """
    List objects in an S3 bucket by prefix.

    :param bucket_name: Name of the bucket to list objects from
    :param prefix: Prefix to filter objects by
    :return: List of object keys
    """
    # fill this out...
    try:
        response = S3_CLIENT.list_objects_v2(Bucket=BUCKET_NAME)
        objects = [content["Key"] for content in response.get("Contents", []) if prefix in content["Key"]]
        return objects
    except ClientError:
        print(f"Failed to list object with given prefix {prefix}")


prefix = "example-a/"
objects_by_prefix = list_all_objects_in_bucket_by_prefix(BUCKET_NAME, prefix)
if objects_by_prefix:
    print(f"Objects with prefix '{prefix}':")
    for obj in objects_by_prefix:
        print(f" - {obj}")
else:
    print(f"No objects found with prefix '{prefix}'.")

# %%
string_test = "temp_item_substr"
"substr" in string_test

# %%
var = 1
result = False or var
print(result)

# %% [markdown]
# ## Exercise 9 - Delete a bucket, no matter what!
#
# In this exercise, you will delete the S3 bucket. Your bucket may have objects in it. Does that matter?
#
# Write a function to delete your bucket.
#
# ***Be careful to point it at the right bucket using the right
# AWS credentials--or you might delete the wrong bucket!***

# %%
import boto3
from botocore.exceptions import ClientError

try:
    from mypy_boto3_s3.type_defs import EmptyResponseMetadataTypeDef
except ImportError:
    print("boto3-stubs[s3] not installed")


def delete_bucket(bucket_name: str) -> Optional["EmptyResponseMetadataTypeDef"]:
    """
    Delete an S3 bucket, including all its objects.

    If the bucket does not exist, no error is raised.

    :param bucket_name: Name of the bucket to delete
    :return: Response from the delete_bucket call or None if there is no bucket.
    """
    # Delete all items in the bucket
    delete_all_objects_in_bucket(bucket_name=bucket_name)

    # Delete bucket
    try:
        response = S3_CLIENT.delete_bucket(Bucket=bucket_name)
        return response
    except ClientError as err:
        if "NoSuchBucket" in str(err):
            return None
        raise


def delete_all_objects_in_bucket(bucket_name: str) -> None:
    """Delete all objects in an S3 bucket. If the bucket does not exist, no error is raised.

    :param bucket_name (str): Name of the bucket to delete objects from
    """
    try:
        object_keys = list_all_object_keys_in_bucket(bucket_name=bucket_name)
    except ClientError as err:
        if "NoSuchBucket" in str(err):
            return None
        raise
    for key in object_keys:
        S3_CLIENT.delete_object(Bucket=bucket_name, Key=key)


response = delete_bucket(BUCKET_NAME)
print(response)

# %% [markdown]
# ## (Optional) Bonus Exercise #1 - Recursively upload a local directory to S3

# %%
from pathlib import Path


def recursively_upload_dir_to_bucket(
    local_dir_fpath: str | Path,
    bucket_name: str,
    target_root_prefix_in_bucket: str = "",
):
    """
    Recurse through a local directory and upload all files to S3 under a target prefix.

    The object keys within the bucket should be the relative paths of the files within the local directory.

    Example:

    path/to/local_dir/
    ├── file1.txt
    ├── file2.txt
    └── subdir
        └── file3.txt

    Would be uploaded to

    s3://bucket-name/target_root_prefix_in_bucket/
    ├── file1.txt
    ├── file2.txt
    └── subdir/
        └── file3.txt
    """
    # fill this out...


# create a test dir locally with sample files
test_dir = Path("test_dir")
test_dir.mkdir(parents=True, exist_ok=True)
(test_dir / "file1.txt").write_text("This is file 1.")
(test_dir / "file2.txt").write_text("This is file 2.")
(test_dir / "subdir").mkdir(parents=True, exist_ok=True)
(test_dir / "subdir" / "file3.txt").write_text("This is file 3.")

# clean up the bucket
delete_bucket(BUCKET_NAME)
create_bucket(bucket_name=BUCKET_NAME)

recursively_upload_dir_to_bucket(
    bucket_name=BUCKET_NAME,
    local_dir_fpath=test_dir,
    target_root_prefix_in_bucket="test-root-dir/",
)

# List all objects in the bucket at the test target root
objects = list_all_objects_in_bucket_by_prefix(
    bucket_name=BUCKET_NAME,
    prefix="test-root-dir/",
)
print(objects)


# %% [markdown]
# ## (Optional) Bonus Exercise #2 - Rename a "folder" in an S3 bucket
#
# S3 is a key-value store for blobs of bytes. There is no way to "rename" a "folder" in S3
# without changing the key names of each object in the "folder".
#
# To really feel the weight and implications of this fact, go through this exercise 🤣
#
# Ultimately, you have to copy each object one at a time, and delete the old object. For large buckets, e.g.
# data lakes with millions of files, this is a slow process.


# %%
def rename_folder_in_bucket(
    bucket_name: str,
    old_folder_prefix: str,
    new_folder_prefix: str,
):
    """
    Rename a "folder" in an S3 bucket.

    Example:

    Given the following structure in S3:

    s3://bucket-name/<old_folder_prefix>/
    ├── file1.txt
    ├── file2.txt
    └── subdir/
        └── file3.txt

    After renaming

    s3://bucket-name/<new_folder_prefix>/
    ├── file1.txt
    ├── file2.txt
    └── subdir/
        └── file3.txt

    :param bucket_name: Name of the S3 bucket
    :param source_folder: Source "folder" path in the bucket
    :param destination_folder: Destination "folder" path in the bucket
    """
    # fill this out...


def move_object_in_bucket(bucket_name: str, source_key: str, destination_key: str):
    """
    Move an object within an S3 bucket by copying to the new key and deleting the old key.

    :param bucket_name: Name of the S3 bucket
    :param source_key: Source key of the object to move
    :param destination_key: Destination key of the object
    """
    # fill this out...


"""Test the rename_folder_in_bucket function."""


def upload_file_to_bucket(
    local_fpath: str | Path,
    bucket_name: str,
    target_key_in_bucket: str,
):
    """
    Upload a file to an S3 bucket.

    :param local_fpath: Local file path to upload
    :param bucket_name: Name of the bucket to upload the file to
    :param target_key_in_bucket: Key to upload the file to in the bucket
    """
    local_fpath = Path(local_fpath)
    with open(local_fpath, "rb") as file:
        S3_CLIENT.put_object(Bucket=bucket_name, Key=target_key_in_bucket, Body=file)


# Create test objects in the source folder
test_source_folder = "nested/source-folder/"
test_dest_folder = "nested/destination-folder/"

create_bucket(bucket_name=BUCKET_NAME)

# Upload test files to source folder
upload_file_to_bucket(
    local_fpath="test_dir/file1.txt", bucket_name=BUCKET_NAME, target_key_in_bucket=test_source_folder + "file1.txt"
)
upload_file_to_bucket(
    local_fpath="test_dir/file2.txt", bucket_name=BUCKET_NAME, target_key_in_bucket=test_source_folder + "file2.txt"
)
upload_file_to_bucket(
    local_fpath="test_dir/subdir/file3.txt",
    bucket_name=BUCKET_NAME,
    target_key_in_bucket=test_source_folder + "subdir/file3.txt",
)

# Rename the source folder to the destination folder
rename_folder_in_bucket(
    bucket_name=BUCKET_NAME,
    old_folder_prefix=test_source_folder,
    new_folder_prefix=test_dest_folder,
)

# List all objects in the destination folder
objects = list_all_objects_in_bucket_by_prefix(bucket_name=BUCKET_NAME, prefix=test_dest_folder)
print(objects)
