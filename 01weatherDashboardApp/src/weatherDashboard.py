import os
import json
import boto3
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class weatherDashboard:
    def __init__(self):
        self.api_key=os.getenv('OPENWEATHER_API_KEY')
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        self.s3_client = boto3.client('s3')

    def create_bucket_if_not_exists(self):
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} exists")
        except:
            print(f"Creating bucket {self.bucket_name}")
        try:
            self.s3_client.create_bucket(Bucket=self.bucket_name)
            print(f"Successfully created bucket {self.bucket_name}")
        except Exception as e:
            print(f"Error creating bucket: {e}")

    def get_weather_data(self, city):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        params = {
            "q" : city,
            "appid" : self.api_key,
            "units" : "imperial"
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print (f"Error fetching weather data: {e}")
            return None
        
    def save_weather_data(self, weather_data, city):
        if not weather_data:
            return False
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f"weather-data/{city}-{timestamp}.json"

        try:
            weather_data['timestamp'] = timestamp
            self.s3_client.put_object (
                Bucket=self.bucket_name,
                Key=file_name,
                Body=json.dumps(weather_data),
                ContentType='application/json'
            )
            print(f"Successfullly saved data for {city} to s3")
            return True
        except Exception as e:
            print (f"Error saving to s3; {e}")
            return False
        
    def get_weather_data_from_s3(self, city):
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=f"weather_data/{city}.json"
            )
            return json.load(response['Body'])
        except Exception as e:
            print(f"Error fetching data from s3 {e}")
            return None
        
def main():
    dashboard = weatherDashboard()
    dashboard.create_bucket_if_not_exists()

    cities = ["Dar es Salaam", "Nairobi", "Kampala", "Lagos", "Accra"]

    for city in cities:
        print(f"\nFetching weather for {city}...")
        weather_data = dashboard.get_weather_data(city)
        if weather_data:
            temp = weather_data['main'] ['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']

            print(f"Temperature: {temp} °F")
            print(f"Feels like: {feels_like} °F")
            print(f"Humidity: {humidity}%")
            print(f"Conditions: {description}")

            success = dashboard.save_weather_data(weather_data, city)
            if success:
                print(f"Weather data for {city} saved successfullly to s3")
            else:
                print(f"Failed to fetch weather data for {city}")

if __name__ == "__main__":
    main()
