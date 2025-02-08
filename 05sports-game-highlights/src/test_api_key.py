import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_URL = os.getenv("API_URL")
RAPID_API_HOST = os.getenv("RAPID_API_HOST")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")

def test_api_key():
    query_params = {
        "countryName": "Australia",
        "limit": 40,
        "homeTeamName": "Adelaide",
        "homeTeamId": 7592,
        "leagueName": "NBL",
        "date": "2023-10-01",
        "season": 2023,
        "timezone": "Etc/UTC",
        "leagueId": 1635,
        "matchId": 299340885,
        "awayTeamId": 1635,
        "awayTeamName": "Melbourne United",
        "countryCode": "AU",
        "offset": 0
    }
    headers = {
        "x-rapidapi-host": RAPID_API_HOST,
        "x-rapidapi-key": RAPID_API_KEY
    }
    response = requests.get(API_URL, headers=headers, params=query_params)
    if response.status_code == 200:
        print("API key is valid. Response:", response.json())
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_api_key()