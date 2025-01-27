import json
import boto3
import requests
import subprocess

from config import (
    API_URL,
    RAPID_API_HOST,
    RAPID_API_KEY,
    DATE,
    LEAGUE_NAME,
    LIMIT,
    S3_BUCKET_NAME,
    INPUT_KEY,
    OUTPUT_KEY,
    AWS_REGION
)

def validate_parameters():
    if not API_URL:
        raise ValueError("API_URL is not set")
    if not RAPID_API_HOST:
        raise ValueError("RAPID_API_HOST is not set")
    if not RAPID_API_KEY:
        raise ValueError("RAPID_API_KEY is not set or is incorrect")
    if not S3_BUCKET_NAME:
        raise ValueError("S3_BUCKET_NAME is not set")
    if not AWS_REGION:
        raise ValueError("AWS_REGION is not set")
    if not DATE:
        raise ValueError("DATE is not set")
    if not LEAGUE_NAME:
        raise ValueError("LEAGUE_NAME is not set")
    if not INPUT_KEY:
        raise ValueError("INPUT_KEY is not set")
    if not OUTPUT_KEY:
        raise ValueError("OUTPUT_KEY is not set")
    if not isinstance(LIMIT, int) or LIMIT <= 0:
        raise ValueError("LIMIT must be a positive integer")

def fetch_highlights():
    try:
        query_params = {
            "date": DATE,
            "league_name": LEAGUE_NAME,
            "limit": LIMIT
        }
        headers = {
            "X-RapidAPI-Host": RAPID_API_HOST,
            "X-RapidAPI-Key": RAPID_API_KEY
        }
        response = requests.get(API_URL, headers=headers, params=query_params, timeout=120)

        response.raise_for_status()

        highlights = response.json()
        return highlights

    except requests.exceptions.RequestException as e:
        print(f"Error fetching highlights: {e}")
        if e.response:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return None

def save_to_s3(data, file_name):
    try:
        s3 = boto3.client("s3", region_name='us-east-1')
        try:
            s3.head_bucket(Bucket=S3_BUCKET_NAME)
            print(f"Bucket {S3_BUCKET_NAME} exists")
        except Exception:
            print(f"Bucket {S3_BUCKET_NAME} does not exist. Creating bucket...")
            if AWS_REGION == "us-east-1":
                s3.create_bucket(Bucket=S3_BUCKET_NAME)
            else:
                s3.create_bucket(
                    Bucket=S3_BUCKET_NAME,
                    CreateBucketConfiguration={
                        "LocationConstraint": AWS_REGION
                    }
                )
            print(f"Bucket {S3_BUCKET_NAME} created successfully!")

        s3_key = f"Highlights/{file_name}.json"

        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(data),
            ContentType="application/json"
        )

        print(f"Highlights saved to S3: s3://{S3_BUCKET_NAME}/{s3_key}")

    except Exception as e:
        print(f"Error saving to S3: {e}")

def convert_media(input_file, output_file):
    try:
        subprocess.run(['ffmpeg', '-i', input_file, output_file], check=True)
        print(f"Media converted successfully: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting media: {e}")

def process_highlights():
    print("Fetching highlights...")

    highlights = fetch_highlights()

    if highlights:
        print("Saving highlights to S3...")
        save_to_s3(highlights, "basketball_highlights")

        s3 = boto3.client("s3", region_name=AWS_REGION)
        input_file = '/tmp/input.json'
        output_file = '/tmp/output.mp4'
        s3.download_file(S3_BUCKET_NAME, INPUT_KEY, input_file)

        convert_media(input_file, output_file)

        s3.upload_file(output_file, S3_BUCKET_NAME, OUTPUT_KEY)
        print(f"Converted media uploaded to S3: s3://{S3_BUCKET_NAME}/{OUTPUT_KEY}")

if __name__ == "__main__":
    process_highlights()