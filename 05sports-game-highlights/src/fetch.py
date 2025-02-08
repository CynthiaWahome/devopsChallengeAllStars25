import json
import boto3
import requests
import subprocess
from botocore.exceptions import NoCredentialsError, ClientError
import os

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

# Print environment variables to verify they are loaded correctly
print(f"API_URL: {API_URL}")
print(f"RAPID_API_HOST: {RAPID_API_HOST}")
print(f"RAPID_API_KEY: {RAPID_API_KEY}")

def fetch_highlights():
    try:
        query_params = {
            "date": DATE,
            "leagueName": LEAGUE_NAME,
            "limit": LIMIT
        }
        headers = {
            "X-RapidAPI-Host": RAPID_API_HOST,
            "X-RapidAPI-Key": RAPID_API_KEY
        }
        
        # Print query parameters to verify they are correct
        print(f"Query Parameters: {query_params}")
        
        response = requests.get(API_URL, headers=headers, params=query_params, timeout=120)

        response.raise_for_status()

        highlights = response.json()

        # Extract the sport name from the API_URL
        sport_name = API_URL.split('/')[-2]

        # Save the entire JSON response to a file named based on the sport
        json_file_name = f'{sport_name}_highlights.json'
        with open(json_file_name, 'w') as f:
            json.dump(highlights, f, indent=4)
        
        # Extract only the "url" fields from the "data" array
        urls = [item["url"] for item in highlights.get("data", []) if "url" in item]
        
        return urls, json_file_name

    except requests.exceptions.RequestException as e:
        print(f"Error fetching highlights: {e}")
        if e.response:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return None, None

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

def download_video(url, local_filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded video: {local_filename}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading video: {e}")
        return False

def convert_media(input_file, output_file):
    try:
        subprocess.run(['ffmpeg', '-i', input_file, '-c:v', 'copy', '-c:a', 'copy', output_file], check=True)
        print(f"Media converted successfully: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting media: {e}")

def process_highlights():
    print("Fetching highlights...")

    urls, json_file_name = fetch_highlights()

    if urls:
        print("Saving highlights to S3...")
        save_to_s3(urls, json_file_name)

        output_folder = 'output_videos'
        raw_folder = os.path.join(output_folder, 'raw')
        converted_folder = os.path.join(output_folder, 'converted')
        
        # Create directories if they do not exist
        os.makedirs(raw_folder, exist_ok=True)
        os.makedirs(converted_folder, exist_ok=True)

        for i, url in enumerate(urls):
            raw_file = os.path.join(raw_folder, f'{json_file_name.split("_")[0]}_highlight_{i}.mp4')
            converted_file = os.path.join(converted_folder, f'output_{i}.mp4')
            
            if download_video(url, raw_file):
                try:
                    convert_media(raw_file, converted_file)
                except subprocess.CalledProcessError as e:
                    print(f"Error converting media: {e}")
                    continue

                if os.path.exists(converted_file):
                    s3 = boto3.client("s3", region_name=AWS_REGION)
                    s3.upload_file(converted_file, S3_BUCKET_NAME, f'output_videos/converted/output_{i}.mp4')
                    print(f"Converted media uploaded to S3: s3://{S3_BUCKET_NAME}/output_videos/converted/output_{i}.mp4")
                else:
                    print(f"Error: Output file {converted_file} was not created.")
            else:
                print(f"Error: Failed to download video from {url}")

if __name__ == "__main__":
    try:
        validate_parameters()
        process_highlights()
    except ValueError as e:
        print(f"Parameter validation error: {e}")