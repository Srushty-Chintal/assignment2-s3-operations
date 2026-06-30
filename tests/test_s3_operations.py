import os
import unittest
import boto3
from moto import mock_aws

from src.s3_operations import S3Operation


class TestS3Operation(unittest.TestCase):

    def setUp(self):
        self.bucket_name = "test-s3-operation-bucket"
        self.region = "us-east-1"

        self.mock_aws = mock_aws()
        self.mock_aws.start()

        self.s3_client = boto3.client("s3", region_name=self.region)
        self.s3_client.create_bucket(Bucket=self.bucket_name)

        self.s3_operation = S3Operation(
            bucket_name=self.bucket_name,
            region_name=self.region
        )

    def tearDown(self):
        self.mock_aws.stop()

        for file_name in [
            "filtered_by_tags.txt",
            "filtered_by_metadata.txt",
            "delete_by_tags.txt",
            "delete_by_metadata.txt"
        ]:
            if os.path.exists(file_name):
                os.remove(file_name)

    def count_objects(self):
        paginator = self.s3_client.get_paginator("list_objects_v2")
        count = 0

        for page in paginator.paginate(Bucket=self.bucket_name):
            count += len(page.get("Contents", []))

        return count

    def test_add_s3_objects(self):
        result = self.s3_operation.add_s3_objects(2500)

        self.assertEqual(result, 2500)
        self.assertEqual(self.count_objects(), 2500)

    def test_fetch_s3_object_by_tags(self):
        self.s3_operation.add_s3_objects(2500)

        result = self.s3_operation.fetch_s3_objects_by_tags(
            tag_key="number-type",
            tag_value="natural",
            output_file="filtered_by_tags.txt"
        )

        self.assertEqual(len(result), 833)
        self.assertTrue(os.path.exists("filtered_by_tags.txt"))

    def test_fetch_s3_object_by_metadata(self):
        self.s3_operation.add_s3_objects(2500)

        result = self.s3_operation.fetch_s3_objects_by_metadata(
            metadata_key="number-type",
            metadata_value="even",
            output_file="filtered_by_metadata.txt"
        )

        self.assertEqual(len(result), 834)
        self.assertTrue(os.path.exists("filtered_by_metadata.txt"))

    def test_delete_s3_object_by_tags(self):
        self.s3_operation.add_s3_objects(2500)

        deleted_count = self.s3_operation.delete_s3_objects_by_tags(
            tag_key="number-type",
            tag_value="natural"
        )

        self.assertEqual(deleted_count, 833)
        self.assertEqual(self.count_objects(), 1667)

    def test_delete_s3_object_by_metadata(self):
        self.s3_operation.add_s3_objects(2500)

        deleted_count = self.s3_operation.delete_s3_objects_by_metadata(
            metadata_key="number-type",
            metadata_value="even"
        )

        self.assertEqual(deleted_count, 834)
        self.assertEqual(self.count_objects(), 1666)


if __name__ == "__main__":
    unittest.main()