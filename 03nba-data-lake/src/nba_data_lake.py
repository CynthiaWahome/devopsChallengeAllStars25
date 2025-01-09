import json
import os
import random
import time
import boto3
import requests
from dotenv import load_dotenv

load_dotenv()

def get_aws_region():
    session = boto3.Session()
    return session.region_name

region = get_aws_region()
random_ints = random.randint(100, 400)
bucket_name = "nba-data-lake-bucket"
bucket_name = f"nba-data-lake-bucket-{random_ints}"

glue_database = "nba_data_lake_db"
athena_output_location = f"s3://{bucket_name}/athena-query-results/"


api_key = os.getenv("NBA_API_KEY")
nba_endpoint = os.getenv("NBA_ENDPOINT")

s3_client = boto3.client("s3", region_name=region)
glue_client = boto3.client("glue", region_name=region)
athena_client = boto3.client("athena", region_name=region)

def create_bucket(bucket_name):
    try:
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
        print(f"S3 bucket '{bucket_name}' created successfully")
    except Exception as e:
        print(f"Error creating S3 bucket: {e}")

def create_glue_database(glue_database):
    try:
        glue_client.create_database(DatabaseInput={"Name": glue_database, "Description": "Glue database for NBA sports analytics."})

        print(f"Glue database '{glue_database}' created successfully")
    except Exception as e:
        print(f"Error creating Glue database: {e}")

def fetch_nba_data():
    try:
        headers = {"Ocp-Apim-Subscription-Key":api_key}
        response = requests.get(nba_endpoint, headers=headers)
        response.raise_for_status()
        print("NBA data fetched successfully")
        return response.json() 
    except Exception as e:
        print(f"Error fetching NBA data: {e}")
        return []
    
def upload_data_to_s3(data):
    try:
        data = fetch_nba_data()
        if data:
            s3_client.put_object(Bucket=bucket_name, Key="nba-data.json", Body=json.dumps(data))
            print("NBA data uploaded to S3 successfully")
        else:
            print("No NBA data to upload to S3 bucket")
    except Exception as e:
        print(f"Error uploading data to S3: {e}")

def create_glue_table():
    try:
        # Define the S3 path where the NBA data is stored
        s3_path = f"s3://{bucket_name}/nba-data.json"
        
        # Define the name of the Glue table
        table_name = "nba_data_table"
        
        # Define the table schema
        columns = [
            {"Name": "player_id", "Type": "int"},
            {"Name": "first_name", "Type": "string"},
            {"Name": "last_name", "Type": "string"},
            {"Name": "position", "Type": "string"},
            {"Name": "team", "Type": "string"}
        ]
        
        # Define the StorageDescriptor
        storage_descriptor = {
            "Columns": columns,
            "Location": s3_path,
            "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
            "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
            "SerdeInfo": {
                "SerializationLibrary": "org.openx.data.jsonserde.JsonSerDe",
                "Parameters": {"serialization.format": "1"}
            }
        }
        
        # Create the Glue table
        glue_client.create_table(
            DatabaseName=glue_database,
            TableInput={
                "Name": table_name,
                "Description": "NBA player data",
                "StorageDescriptor": storage_descriptor,
                "TableType": "EXTERNAL_TABLE",
                "Parameters": {"classification": "json"}
            }
        )
        
        # Print a success message if the table is created successfully
        print(f"Glue table '{table_name}' created successfully")
    except Exception as e:
        # Print an error message if there is an issue creating the table
        print(f"Error creating Glue table: {e}")


def configure_athena():
    try:
        athena_client.start_query_execution(
            QueryString="CREATE DATABASE IF NOT EXISTS nba_athena_db",
            QueryExecutionContext={"Database":glue_database},
            ResultConfiguration={"OutputLocation": athena_output_location},
        )
        print("Athena output location configured successfully")
    except Exception as e:
        print(f"Error configuring Athena: {e}")

def main():
    print("Setting up data lake from NBA sports analytics")
    create_bucket(bucket_name)
    time.sleep(5)
    create_glue_database(glue_database)
    nba_data = fetch_nba_data()
    if nba_data:
        upload_data_to_s3(nba_data)
    else:
        print("No NBA data to upload to S3 bucket")

    create_glue_table()
    configure_athena()
    print("NBA data lake setup complete")

if __name__ == "__main__":
    main()