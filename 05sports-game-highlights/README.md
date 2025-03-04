# NCAAGameHighlights

## Introduction
NCAAGameHighlights is a project that uses RapidAPI to obtain NCAA game highlights. The project leverages Docker for containerization and FFmpeg for media file conversion.

## HighlightProcessor
This project uses RapidAPI to obtain NCAA game highlights using a Docker container and uses FFmpeg to convert the media file.

# File Overview

- **`config.py`**: Imports environment variables and assigns them to Python variables, providing default values where appropriate.
- **`fetch.py`**: Fetches highlights from the API and stores them in an S3 bucket as a JSON file.
- **`process_one_video.py`**: Retrieves the JSON file from S3, downloads the video, and saves it back to S3.
- **`ffmpeg_process.py`**: Uses FFmpeg to process a video file and stores the processed video back into S3.
- **`run_all.py`**: Runs the scripts in order and provides buffer time for task creation.
- **`.env`**: Stores environment variables.
- **`Dockerfile`**: Provides steps to build the Docker image.
- **Terraform Scripts**: Creates AWS resources in a scalable and repeatable way.

## Technical Diagram
![GameHighlightProcessor](https://github.com/user-attachments/assets/762c3582-c6fe-48b2-b7da-0ff5b86b7970)

## Project Structure
```bash
src/
├── Dockerfile
├── config.py
├── fetch.py
├── ffmpeg_process.py
├── process_one_video.py
├── requirements.txt
├── run_all.py
├── .env
## Installation

1. Clone the repository:
	```bash
	git clone https://github.com/yourusername/NCAAGameHighlights.git
	cd NCAAGameHighlights/src
	```

2. Build the Docker image:
	```bash
	docker build -t ncaagamehighlights .
	```

3. Create a `.env` file with the necessary environment variables.

## Usage

1. Run the Docker container:
	```bash
	docker run --env-file .env ncaagamehighlights
	```

2. Follow the steps in `run_all.py` to fetch and process the game highlights.

## Setup Guide

For detailed step-by-step instructions on setting up and running the project, please refer to the SETUP.md file.

## Future Enhancements
1. Using Terraform to enhance the Infrastructure as Code (IaC).
2. Increasing the number of videos processed and converted with FFmpeg.
3. Change the date from static (specific point in time) to dynamic (now, last 30 days from today's date, etc).
```