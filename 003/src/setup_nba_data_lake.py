import json
import os
import sys
import time

import boto3
import requests
from dotenv import load_dotenv

load_dotenv()

# AWS configurations
region                 =  os.getenv("region","us-east-1")
bucket_name            =  os.getenv("bucket_name")
raw_data_key           =  os.getenv("glue_table_name") 
# raw_data_key, Set to same as table name, so the crawler can overwrite the existing table
glue_role_arn          =  os.getenv("glue_role_arn")
glue_database_name     =  os.getenv("glue_database_name")
glue_table_name        =  os.getenv("glue_table_name")
glue_crawler_name      =  os.getenv("glue_crawler_name")
athena_output_location =  f"s3://{bucket_name}/athena-results/"

# Sportsdata.io configurations (loaded from .env)
api_key                = os.getenv("SPORTS_DATA_API_KEY")
nba_endpoint           = os.getenv("NBA_ENDPOINT") 

# Create AWS clients
s3_client     = boto3.client("s3",     region_name=region)
glue_client   = boto3.client("glue",   region_name=region)
athena_client = boto3.client("athena", region_name=region)

def create_s3_bucket():
    """Create an S3 bucket for storing sports data."""
    try:
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
        print(f"S3 bucket '{bucket_name}' created successfully.")
    except Exception as e:
        print(f"Error creating S3 bucket: {e}")

def create_glue_database():
    """Create a Glue database for the data lake."""
    try:
        glue_client.create_database(
            DatabaseInput={
                "Name": glue_database_name,
                "Description": "Glue database for NBA sports analytics.",
            }
        )
        print(f"Glue database '{glue_database_name}' created successfully.")
    except Exception as e:
        print(f"Error creating Glue database: {e}")

def fetch_nba_data():
    """Fetch NBA player data from sportsdata.io."""
    try:
        headers = {"Ocp-Apim-Subscription-Key": api_key}
        response = requests.get(nba_endpoint, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        print("Fetched NBA data successfully.")
        return response.json()  # Return JSON response
    except Exception as e:
        print(f"Error fetching NBA data: {e}")
        return []

def convert_to_line_delimited_json(data):
    """Convert data to line-delimited JSON format."""
    print("Converting data to line-delimited JSON format...")
    return "\n".join([json.dumps(record) for record in data])

def upload_data_to_s3(data):
    """Upload NBA data to the S3 bucket."""
    try:
        # Convert data to line-delimited JSON
        line_delimited_data = convert_to_line_delimited_json(data)

        # Define S3 object key
        file_key = f"{raw_data_key}/nba_player_data.jsonl"

        # Upload JSON data to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=line_delimited_data
        )
        print(f"Uploaded data to S3: {file_key}")
    except Exception as e:
        print(f"Error uploading data to S3: {e}")

def create_glue_table():
    """Create a Glue table for the data."""
    try:
        glue_client.create_table(
            DatabaseName=glue_database_name,
            TableInput={
                "Name": glue_table_name,
                "StorageDescriptor": {
                    "Columns": [
                        {"Name": "PlayerID", "Type": "int"},
                        {"Name": "Status", "Type": "string"},
                        {"Name": "FirstName", "Type": "string"},
                        {"Name": "LastName", "Type": "string"},
                        {"Name": "Team", "Type": "string"},
                        {"Name": "Height", "Type": "int"},
                        {"Name": "Weight", "Type": "int"},
                    ],
                    "Location": f"s3://{bucket_name}/{raw_data_key}/",
                    "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                    "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                    "SerdeInfo": {
                        "SerializationLibrary": "org.openx.data.jsonserde.JsonSerDe"
                    },
                },
                "TableType": "EXTERNAL_TABLE",
            },
        )
        print(f"Glue table {glue_table_name} created successfully.")
    except Exception as e:
        print(f"Error creating Glue table: {e}")


def create_glue_crawler():
    try:
        glue_client.create_crawler(
            Name=glue_crawler_name,
            Role=glue_role_arn,
            DatabaseName=glue_database_name,
            Description='to crawl my nba data',
            Targets={
                'S3Targets': [
                    {
                        'Path': f"s3://{bucket_name}/{raw_data_key}/",
                    },
                ],
            },
            # Schedule="cron(0 18 */2 * ? *)",
            # TablePrefix="nba_",
            SchemaChangePolicy={
                "UpdateBehavior": "UPDATE_IN_DATABASE",
                "DeleteBehavior": "LOG" 
            },
            # RecrawlPolicy={
            #     "RecrawlBehavior": "CRAWL_NEW_FOLDERS_ONLY"
            # }


        )
    except glue_client.exceptions.AlreadyExistsException:
        print(f"Glue crawler {glue_crawler_name} already exists.")
    except Exception as e:
        print(f"Error creating Glue crawler: {e}")


def run_glue_crawler():
    print("Running glue crawler...")
    try:
        glue_client.start_crawler(Name=glue_crawler_name)
        print(f"Glue crawler {glue_crawler_name} started successfully.")
    except Exception as e:
        print(f"Error starting Glue crawler: {e}")


def configure_athena():
    """Set up Athena output location."""
    try:
        athena_client.start_query_execution(
            QueryString           = f"SELECT * FROM {glue_database_name}.{glue_table_name}",
            QueryExecutionContext = {"Database": glue_database_name},
            ResultConfiguration   = {"OutputLocation": athena_output_location},
        )
        print("Athena output location configured successfully.")
    except Exception as e:
        print(f"Error configuring Athena: {e}")

# Main workflow
def main():
    print("Setting up data lake for NBA sports analytics...")
    create_s3_bucket()
    time.sleep(5)                # Ensure bucket creation propagates
    create_glue_database()
    nba_data = fetch_nba_data()
    if not nba_data:             # Only proceed if data was fetched successfully
        sys.exit(1)                   #stop run if no data
    upload_data_to_s3(nba_data)
    create_glue_table()
    create_glue_crawler()
    configure_athena()
    run_glue_crawler() 
    print("Data lake setup complete.")
    

if __name__ == "__main__":
    main()