from moto import mock_aws
import boto3

from src.s3_operations import S3Operation


@mock_aws
def test_add_s3_objects():

    bucket_name = "test-bucket"

    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    s3_operation = S3Operation(bucket_name)

    result = s3_operation.add_s3_objects(
        object_name="test.txt",
        content="Hello AWS",
        tags="department=IT",
        metadata={"department": "IT"}
    )

    assert result == "test.txt uploaded successfully"


@mock_aws
def test_fetch_s3_objects_by_metadata():

    bucket_name = "test-bucket"

    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    s3_operation = S3Operation(bucket_name)

    s3_operation.add_s3_objects(
        object_name="student.txt",
        content="Student Data",
        metadata={"department": "IT"}
    )

    result = s3_operation.fetch_s3_objects_by_metadata()

    assert len(result) == 1


@mock_aws
def test_delete_s3_objects():

    bucket_name = "test-bucket"

    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=bucket_name)

    s3_operation = S3Operation(bucket_name)

    s3_operation.add_s3_objects(
        object_name="delete.txt",
        content="Delete Me"
    )

    result = s3_operation.delete_s3_objects_by_tags()

    assert result == "Objects deleted successfully"