import boto3
from time import sleep
import os
import json

# references
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html
# https://docs.localstack.cloud/user-guide/aws/s3/

# create localstack bucket on cli
# awslocal s3api create-bucket --bucket my-bucket-name --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2


class S3Client():
    def __init__(self, url: str) -> None:
        self.url = url
        self.bucket = "test"
        self.client = self.config()

    def config(self) -> boto3.client:
        session = boto3.Session()
        return session.client(
            's3',
            region_name=os.environ.get('AWS_REGION'),
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            endpoint_url=self.url
        )

    def list_buckets(self) -> list:
        response = self.client.list_buckets()
        print("Buckets:")
        for bucket in response['Buckets']:
            print(f'    {bucket["Name"]}')

    def load_file(self, fname: str) -> bool:
        object_name = os.path.basename(fname)
        try:
            response = self.client.upload_file(fname, self.bucket, object_name)
        except Exception as e:
            print(f"There was an error loading the file: {e}")
        print(f"{fname} loaded successfully!")

    def download_file(self, fname: str) -> bool:
        try:
            savename = f"{fname.split('.')[0]}_download.json"
            self.client.download_file(self.bucket, fname, savename)
        except Exception as e:
            print(f"There was an error loading the file: {e}")
        print(f"{fname} downloaded successfully!")

    def read_file(self, fname: str) -> bool:
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=fname)
            print(json.loads(response['Body'].read().decode('utf-8')))
        except Exception as e:
            print(f"There was an error reading the file: {e}")


if __name__ == '__main__':
    # vars
    url = "http://localhost:4566/"  # "http://test.s3.localhost.localstack.cloud:4566/" # can also reference bucket directly
    fname = 'dummy_data/donuts.json'

    # get the client
    s3 = S3Client(url)

    # list buckets
    # s3.list_buckets()

    # load file
    # s3.load_file(fname)

    # download file
    # s3.download_file(fname)

    # read file
    s3.read_file(fname)
