import json
import os

from s3_operations import S3Operation


def lambda_handler(event, context):
    bucket_name = os.environ["BUCKET_NAME"]

    s3_operation = S3Operation(bucket_name)

    uploaded_count = s3_operation.add_s3_objects(2500)

    tag_filtered = s3_operation.fetch_s3_objects_by_tags(
        tag_key="number-type",
        tag_value="natural"
    )

    metadata_filtered = s3_operation.fetch_s3_objects_by_metadata(
        metadata_key="number-type",
        metadata_value="even"
    )

    deleted_by_tags = s3_operation.delete_s3_objects_by_tags(
        tag_key="number-type",
        tag_value="odd"
    )

    deleted_by_metadata = s3_operation.delete_s3_objects_by_metadata(
        metadata_key="number-type",
        metadata_value="even"
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "uploaded_objects": uploaded_count,
            "tag_filtered_objects": len(tag_filtered),
            "metadata_filtered_objects": len(metadata_filtered),
            "deleted_by_tags": deleted_by_tags,
            "deleted_by_metadata": deleted_by_metadata
        })
    }