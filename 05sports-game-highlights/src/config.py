import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "https://sport-highlights-api.p.rapidapi.com/basketball/highlights")

RAPID_API_HOST = os.getenv("RAPIDAPI_HOST", "sport-highlights-api.p.rapidapi.com")

RAPID_API_KEY = os.getenv("RAPIDAPI_KEY")

DATE = os.getenv("DATE", "2023-12-01")

LEAGUE_NAME = os.getenv("LEAGUE_NAME", "NCAA")

LIMIT = int(os.getenv("LIMIT", "10"))

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

INPUT_KEY = os.getenv("INPUT_KEY", "highlights/basketball_highlights.json")

OUTPUT_KEY = os.getenv("OUTPUT_KEY", "videos/first_video.mp4")


RETRY_COUNT = int(os.getenv("RETRY_COUNT", "3"))

RETRY_DELAY = int(os.getenv("RETRY_DELAY", "30"))

WAIT_TIME_BETWEEN_SCRIPTS = int(os.getenv("WAIT_TIME_BETWEEN_SCRIPTS", "60"))
