import json
import boto3
import requests

from io import BytesIO

from config import (
    S3_BUCKET_NAME,
    AWS_REGION,
    INPUT_KEY,
    OUTPUT_KEY
)

def process_one_video():
    try:
        s3 = boto3.client("s3", region_name=AWS_REGION)
        print("Fetching JSON file from S3")
        try:
            response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=INPUT_KEY)
        except s3.exceptions.NoSuchKey:
            print(f"Error: The key {INPUT_KEY} does not exist.")
            return
        except s3.exceptions.NoSuchBucket:
            print(f"Error: The bucket {S3_BUCKET_NAME} does not exist.")
            return
        json_content = response['Body'].read().decode('utf-8')
        highlights = json.loads(json_content)
        video_url = highlights["data"][0]["url"]
        print(f"Processing video URL: {video_url}")
        print("Downloading video...")
        video_response = requests.get(video_url)
        video_response.raise_for_status()
        video_data = BytesIO(video_response.content)
        print("Uploading video to S3...") 

        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=OUTPUT_KEY,
            Body=video_data,
            ContentType="video/mp4"
        )
        print(f"Video uploaded successfully: s3://{S3_BUCKET_NAME}/{OUTPUT_KEY}")
        print(f"Video uploaded successfully: s3://{S3_BUCKET_NAME}/{OUTPUT_KEY}")

    except Exception as e:
        print(f"Error during video processing: {e}")

if __name__ =="__main__":
    process_one_video()