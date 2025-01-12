import boto3
from mypy_boto3_s3 import S3Client

try:
    from mypy_boto3_s3.type_defs import (
        PutObjectOutputTypeDef,
        ResponseMetadataTypeDef,
    )
except ImportError:
    print("boto3-stubs not installed")

BUCKET_NAME = "cloud-course-bucket-betsy"

session = boto3.Session()
s3_client: "S3Client" = session.client("s3")

# Upload to s3
response: "PutObjectOutputTypeDef" = s3_client.put_object(
    Bucket=BUCKET_NAME,
    Key="folder/hello.txt",
    Body="Hello, World!",
    ContentType="text/plain",
)

metadata: "ResponseMetadataTypeDef" = response["ResponseMetadata"]
