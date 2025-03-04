# Setup Guide for NCAAGameHighlights

## Prerequisites
Before setting up the project, ensure you have the following installed:

- **Docker**: `docker --version`
- **AWS CLI**: `aws --version`
- **Python 3**: `python3 --version`
- **FFmpeg**: `ffmpeg -version`

## 1. Clone the Repository
```bash
git clone https://github.com/your-username/NCAAGameHighlights.git
cd NCAAGameHighlights
```

## 2. Set Up Environment Variables
Create a `.env` file in the root directory with the following:
```
RAPIDAPI_KEY=your_rapidapi_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
S3_BUCKET_NAME=your_s3_bucket_name
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Fetch Game Highlights
```bash
python fetch.py
```
This retrieves highlights from RapidAPI and stores them in an S3 bucket as a JSON file.

## 5. Process the Video with FFmpeg
```bash
python process_one_video.py
```
This:
- Downloads the video from the JSON file.
- Stores it in an S3 bucket.

## 6. Convert Video Format with FFmpeg
```bash
python ffmpeg_process.py
```
This script:
- Uses FFmpeg to process the video.
- Adjusts the codec, resolution, and bitrate.
- Stores the processed video in an S3 bucket.

## 7. Run Everything in Order
```bash
python run_all.py
```
This script runs all processes sequentially.

## 8. Docker Setup (Optional)
To containerize the application:
```bash
docker build -t ncaagamehighlights .
docker run --env-file .env ncaagamehighlights
```

## 9. Verify Processed Videos
Check your S3 bucket for the processed video files.
