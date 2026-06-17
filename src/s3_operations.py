import boto3


class S3Operation:

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3")

    def add_s3_objects(self, object_name, content, tags=None, metadata=None):

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=object_name,
            Body=content,
            Metadata=metadata or {},
            Tagging=tags or ""
        )

        return f"{object_name} uploaded successfully"

    def fetch_s3_objects_by_tags(self):

        response = self.s3_client.list_objects_v2(
            Bucket=self.bucket_name
        )

        objects = []

        if "Contents" in response:

            for obj in response["Contents"]:

                key = obj["Key"]

                tag_response = self.s3_client.get_object_tagging(
                    Bucket=self.bucket_name,
                    Key=key
                )

                objects.append({
                    "object": key,
                    "tags": tag_response["TagSet"]
                })

        return objects

    def fetch_s3_objects_by_metadata(self):

        response = self.s3_client.list_objects_v2(
            Bucket=self.bucket_name
        )

        objects = []

        if "Contents" in response:

            for obj in response["Contents"]:

                key = obj["Key"]

                metadata = self.s3_client.head_object(
                    Bucket=self.bucket_name,
                    Key=key
                )

                objects.append({
                    "object": key,
                    "metadata": metadata["Metadata"]
                })

        return objects

    def delete_s3_objects_by_tags(self):

        response = self.s3_client.list_objects_v2(
            Bucket=self.bucket_name
        )

        if "Contents" in response:

            for obj in response["Contents"]:

                self.s3_client.delete_object(
                    Bucket=self.bucket_name,
                    Key=obj["Key"]
                )

        return "Objects deleted successfully"

    def delete_s3_objects_by_metadata(self):

        return self.delete_s3_objects_by_tags()