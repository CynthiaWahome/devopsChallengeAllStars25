import subprocess
import boto3
import os
from config import (
    AWS_REGION,
    S3_BUCKET_NAME,
    INPUT_KEY,
    OUTPUT_KEY
)

def process_video_file(input_file, output_file):
    try:
        subprocess.run(['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-b:v', '5000k', '-c:a', 'aac', '-b:a', '128k', output_file], check=True)
        print(f"Video processed successfully: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing video with FFmpeg: {e}")

def download_from_s3(s3_client, bucket_name, s3_key, local_path):
    try:
        s3_client.download_file(bucket_name, s3_key, local_path)
        print(f"Downloaded {s3_key} from S3 to {local_path}")
    except Exception as e:
        print(f"Error downloading from S3: {e}")

def upload_to_s3(s3_client, local_path, bucket_name, s3_key):
    try:
        s3_client.upload_file(local_path, bucket_name, s3_key)
        print(f"Uploaded {local_path} to S3 at {s3_key}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

def main():
    s3_client = boto3.client("s3", region_name=AWS_REGION)

    local_input_path = '/tmp/input_video.mp4'
    local_output_path = '/tmp/output_video.mp4'

    download_from_s3(s3_client, S3_BUCKET_NAME, INPUT_KEY, local_input_path)
    process_video_file(local_input_path, local_output_path)

    upload_to_s3(s3_client, local_output_path, S3_BUCKET_NAME, OUTPUT_KEY)

if __name__ == "__main__":
    main()