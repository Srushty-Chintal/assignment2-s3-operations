from urllib.parse import urlencode
import boto3


class S3Operation:
    def __init__(self, bucket_name, region_name="us-east-1"):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3", region_name=region_name)

    def add_s3_objects(self, total_objects=2500):
        tag_values = ["natural", "even", "odd"]

        for i in range(1, total_objects + 1):
            category = tag_values[i % 3]

            key = f"numbers/number_{i}.txt"
            content = f"This is natural number {i}"

            metadata = {
                "number-type": category,
                "created-by": "boto3"
            }

            tags = {
                "number-type": category,
                "created-by": "assignment"
            }

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=content.encode("utf-8"),
                Metadata=metadata,
                Tagging=urlencode(tags)
            )

        return total_objects

    def get_all_object_keys(self):
        paginator = self.s3_client.get_paginator("list_objects_v2")
        keys = []

        for page in paginator.paginate(Bucket=self.bucket_name):
            for obj in page.get("Contents", []):
                keys.append(obj["Key"])

        return keys

    def fetch_s3_objects_by_tags(
        self,
        tag_key,
        tag_value,
        output_file="/tmp/filtered_by_tags.txt"
    ):
        matched_keys = []

        for key in self.get_all_object_keys():
            response = self.s3_client.get_object_tagging(
                Bucket=self.bucket_name,
                Key=key
            )

            tags = {
                tag["Key"]: tag["Value"]
                for tag in response.get("TagSet", [])
            }

            if tags.get(tag_key) == tag_value:
                matched_keys.append(key)

        with open(output_file, "w", encoding="utf-8") as file:
            for key in matched_keys:
                file.write(key + "\n")

        return matched_keys

    def fetch_s3_objects_by_metadata(
        self,
        metadata_key,
        metadata_value,
        output_file="/tmp/filtered_by_metadata.txt"
    ):
        matched_keys = []

        for key in self.get_all_object_keys():
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=key
            )

            metadata = response.get("Metadata", {})

            if metadata.get(metadata_key) == metadata_value:
                matched_keys.append(key)

        with open(output_file, "w", encoding="utf-8") as file:
            for key in matched_keys:
                file.write(key + "\n")

        return matched_keys

    def delete_s3_objects_by_tags(self, tag_key, tag_value):
        keys_to_delete = self.fetch_s3_objects_by_tags(
        tag_key,
        tag_value,
        output_file="/tmp/delete_by_tags.txt"
    )

        self._delete_objects(keys_to_delete)

        return len(keys_to_delete)
    
    def delete_s3_objects_by_metadata(self, metadata_key, metadata_value):
        keys_to_delete = self.fetch_s3_objects_by_metadata(
        metadata_key,
        metadata_value,
        output_file="/tmp/delete_by_metadata.txt"
    )

        self._delete_objects(keys_to_delete)

        return len(keys_to_delete)
    def _delete_objects(self, keys):
        for i in range(0, len(keys), 1000):
            batch = keys[i:i + 1000]

            if batch:
                self.s3_client.delete_objects(
                    Bucket=self.bucket_name,
                    Delete={
                        "Objects": [{"Key": key} for key in batch],
                        "Quiet": True
                    }
                )