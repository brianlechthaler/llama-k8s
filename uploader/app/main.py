from boto3 import client
from os import environ


class Uploader:
    def __init__(self):
        self.s3_client = client(
            's3',
            aws_access_key_id=environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY'],
            endpoint_url=f"https://object.{environ['BUCKET_REGION']}.coreweave.com",
            region_name='default'
            )

    def create_bucket(self):
        response = self.s3_client.create_bucket(Bucket=environ['BUCKET_NAME'])
        print(f"Bucket created: {response}")

    def upload_file(self):
        response = self.s3_client.upload_file(environ['FILE_PATH'], environ['BUCKET_NAME'], environ['FILE_NAME'])
        print(f"Uploaded file: {response}")

    def cli_handler(self, operation):
        if operation == 'create_bucket':
            self.create_bucket()
        if operation == 'upload_file':
            self.upload_file()


if __name__ == '__main__':
    runtime = Uploader()
    runtime.cli_handler(environ['OPERATION'])
