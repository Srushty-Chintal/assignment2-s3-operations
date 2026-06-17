import os
from s3_operations import S3Operation


def lambda_handler(event, context):
    bucket_name = os.environ["BUCKET_NAME"]

    s3_operation = S3Operation(bucket_name)

    s3_operation.add_s3_objects(
        object_name="student-1.txt",
        content="Assignment 2 object 1",
        tags="department=IT&year=2026",
        metadata={"department": "IT", "year": "2026"}
    )

    s3_operation.add_s3_objects(
        object_name="student-2.txt",
        content="Assignment 2 object 2",
        tags="department=CS&year=2026",
        metadata={"department": "CS", "year": "2026"}
    )

    objects_by_tags = s3_operation.fetch_s3_objects_by_tags()
    objects_by_metadata = s3_operation.fetch_s3_objects_by_metadata()

    return {
        "statusCode": 200,
        "message": "Assignment 2 S3 operations executed successfully",
        "objects_by_tags": objects_by_tags,
        "objects_by_metadata": objects_by_metadata
    }