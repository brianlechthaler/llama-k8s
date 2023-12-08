from boto3 import client
from os import environ

s3_client = client(
    's3',
    aws_access_key_id=environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY'],
    endpoint_url=environ['ENDPOINT_URL'],
    region_name='default'
)

def create_bucket():
    response = s3_client.create_bucket(Bucket=environ['BUCKET_NAME'])
    print(f"Bucket created: {response}")

if __name__ == '__main__':
    if environ['OPERATION'] == 'create_bucket':
        create_bucket()