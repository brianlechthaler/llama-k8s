from boto3 import client
from os import environ
from os.path import getsize
from math import ceil


class Uploader:
    def __init__(self):
        self.s3_client = client(
            's3',
            aws_access_key_id=environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY'],
            endpoint_url=f"https://object.{environ['BUCKET_REGION']}.coreweave.com",
            region_name='default'
            )
        self.response = None
        self.parts = []

    def create_bucket(self):
        print(f"Creating bucket with name {environ['BUCKET_NAME']}...")
        self.response = self.s3_client.create_bucket(Bucket=environ['BUCKET_NAME'])
        print(f"Bucket created: {self.response}")

    def multipart_upload(self):
        self.response = self.s3_client.create_multipart_upload(Bucket=environ['BUCKET_NAME'],
                                                               Key=environ['FILE_NAME'])
        upload_id = self.response['UploadId']
        print(f"Created Upload ID: {upload_id}")
        part_size = 256 * 1024 * 1024
        file = open(environ['FILE_PATH'], "rb")
        nparts = ceil(getsize(environ['FILE_PATH']) / part_size)
        for index in range(1, nparts+1):
            self.response = self.s3_client.upload_part(
                Bucket=environ['BUCKET_NAME'],
                Key=environ['FILE_NAME'],
                PartNumber=index,
                UploadId=upload_id,
                Body=file.read(part_size)
            )
            self.parts.append({'PartNumber': index, 'ETag': self.response['ETag']})
            print(f"Uploaded part {index} of {nparts}")
        self.s3_client.complete_multipart_upload(Bucket=environ['BUCKET_NAME'],
                                                 Key=environ['FILE_NAME'],
                                                 UploadId=upload_id,
                                                 MultipartUpload={'Parts': self.parts}
                                                 )
        print('Upload complete.')

    def cli_handler(self, operation):
        if operation == 'create_bucket':
            self.create_bucket()
        if operation == 'upload_file':
            self.multipart_upload()
        if operation not in ['create_bucket', 'upload_file']:
            raise Exception("Invalid operation or no operation specified.")


if __name__ == '__main__':
    print("Initializing uploader...")
    runtime = Uploader()
    print(f"Uploader initialized. Now performing action: {environ['OPERATION']}")
    runtime.cli_handler(environ['OPERATION'])
