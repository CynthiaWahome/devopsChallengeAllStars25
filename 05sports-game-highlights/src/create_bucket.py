import boto3
import uuid
from dotenv import load_dotenv, set_key
import os

# Load existing .env file
load_dotenv(dotenv_path='.env')

def create_bucket_with_random_name(region):
    # Generate a random bucket name
    bucket_name = f"my-bucket-{uuid.uuid4()}"

    # Create the S3 client
    s3_client = boto3.client('s3', region_name=region)

    # Create the bucket
    try:
        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': region
                }
            )
        print(f"Bucket created successfully: {bucket_name}")

        # Update the .env file with the new bucket name
        set_key('.env', 'S3_BUCKET_NAME', bucket_name)
        print(f".env file updated with new bucket name: {bucket_name}")

    except Exception as e:
        print(f"Error creating bucket: {e}")

if __name__ == "__main__":
    create_bucket_with_random_name('us-east-1')