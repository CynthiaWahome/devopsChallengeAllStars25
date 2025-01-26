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
    OUTPUT_KEY
)

def fetch_highlights():
    try:
        query_params = {
            "date": DATE,
            "league_name": LEAGUE_NAME,
            "limit": LIMIT
        }
        headers = {
            "X-RapidAPI-Host": RAPIDAPI_HOST,
            "X-RapidAPI-Key": RAPIDAPI_KEY
        }
        response = requests.get(API_URL, headers=headers, params=query_params, timeout=120)

        response.raise_for_status()

        highlights = response.json()
        return highlights

    except requests.exceptions.RequestException as e:
        print(f"Error fetching highlights: {e}")

        return home

def save_to_s3(data, file_name):
    try:
        s3 = boto3.client("s3", region_name=AWS_REGION)
        try:
            s3.head_bucket(Bucket=S3_BUCKET_NAME)
            print(f"Bucket {S3_BUCKET_NAME} exists")
        except Exception:
            print(f"Bucket {S3_BUCKET_NAME} does not exist. Creating bucket...")
            if AWS_REGION == "us-east-1":
                s3.create_bucket(Bucket=S3_BUCKET_NAME)
            else:
                s3.create_bucket{
                    Bucket=S3_BUCKET_NAME,
                    CreateBucketConfiguration={
                        "LocationConstraint": AWS_REGION
                    }
                }
            print(f"Bucket {S3_BUCKET_NAME} created successfully!")

        s3_key = f"Highlights/{file_name}.json"

        s3.put_object{
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(data),
            Content-Type="application/json"
        }

        print(f"Highlights saved to S3: s3://{S3_BUCKET_NAME}/{s3_key}")

    except Exception as e:
        print(f"Error saving to S3: {e}")

    def convert_media(input_file, output_file):
        try:
            subprocess.run(['ffmpeg', '-i', input_file, output_file, check=True])
            print(f"Media converted successfully: {output_file}")
        except sub.process.CalledProcessError as e:
            print(f"Error converting media: {e}")

    def process_highlights():
        print("Fetching highlights...")

        highlights = fetch_highlights()

        if highlights:
            print("Saving highlights to S3...")
            save_to_s3(highlights,"basketball_highlights")

            s3 = boto3.client("s3", region_name=AWS_REGION)
            input_file = '/tmp/input.json'
            output_file = '/tmp/ouput.mp4'
            s3.download_file(S3_BUCKET_NAME, INPUT_KEY, input_file)

            convert_media(input_file, output_file)

            s3.upload_file(output_file, S3_BUCKET_NAME, OUTPUT_KEY)
            print(f"Converted media uploaded to S3: s3://{S3_BUCKET_NAME}/{OUTPUT_KEY}")

if __name__ == "__main__":
    process_highlights()
