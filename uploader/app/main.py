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
        print(f"Creating bucket with name {environ['BUCKET_NAME']}...")
        response = self.s3_client.create_bucket(Bucket=environ['BUCKET_NAME'])
        print(f"Bucket created: {response}")

    def upload_file(self):
        print(f"Opening file at path {environ['FILE_PATH']}...")
        file = open(environ['FILE_PATH'], 'rb')
        print(f"File opened. Uploading...")
        response = self.s3_client.put_object(
            Bucket=environ['BUCKET_NAME'],
            Key=environ['FILE_NAME'],
            Body=file,
            ACL='private'
        )
        print(f"Uploaded file: {response}")

    def cli_handler(self, operation):
        if operation == 'create_bucket':
            self.create_bucket()
        if operation == 'upload_file':
            self.upload_file()
        if operation not in ['create_bucket', 'upload_file']:
            raise Exception("Invalid operation or no operation specified.")


if __name__ == '__main__':
    print("Initializing uploader...")
    runtime = Uploader()
    print(f"Uploader initialized. Now performing action: {environ['OPERATION']}")
    runtime.cli_handler(environ['OPERATION'])
