#fetch.py
import json
import boto3
import requests

from config import (
    API_URL,
    RAPIDAPI_HOST,
    RAPIDAPI_KEY,
    DATE,
    LEAGUE_NAME,
    LIMIT,
    S3_BUCKET_NAME,
    AWS_REGION,
    DYNAMODB_TABLE,
)

def fetch_highlights():
    """
    Fetch basketball highlights from the API.
    """
    try:
        query_params = {
            "date": DATE,
            "leagueName": LEAGUE_NAME,
            "limit": LIMIT
        }
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }

        response = requests.get(API_URL, headers=headers, params=query_params, timeout=120)
        response.raise_for_status()
        highlights = response.json()
        print("Highlights fetched successfully!")
        return highlights
    except requests.exceptions.RequestException as e:
        print(f"Error fetching highlights: {e}")
        return None

def save_to_s3(data, file_name):
    """
    Save data to an S3 bucket.
    """
    try:
        s3 = boto3.client("s3", region_name=AWS_REGION)

        # Check if the bucket exists, if not create it
        try:
            s3.head_bucket(Bucket=S3_BUCKET_NAME)
            print(f"Bucket {S3_BUCKET_NAME} exists.")
        except Exception:
            print(f"Bucket {S3_BUCKET_NAME} does not exist. Creating...")
            if AWS_REGION == "us-east-1":
                s3.create_bucket(Bucket=S3_BUCKET_NAME)
            else:
                s3.create_bucket(
                    Bucket=S3_BUCKET_NAME,
                    CreateBucketConfiguration={"LocationConstraint": AWS_REGION}
                )
            print(f"Bucket {S3_BUCKET_NAME} created successfully.")

        s3_key = f"highlights/{file_name}.json"

        # Upload JSON data
        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(data),
            ContentType="application/json"
        )
        print(f"Highlights saved to S3: s3://{S3_BUCKET_NAME}/{s3_key}")
    except Exception as e:
        print(f"Error saving to S3: {e}")

def store_highlights_to_dynamodb(highlights):
    """
    Store each highlight record into a DynamoDB table.
    Assumes that 'highlights' is a dict with a "data" key that is a list of records.
    """
    try:
        dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
        table = dynamodb.Table(DYNAMODB_TABLE)
        
        # Iterate over each highlight record and store it.
        for record in highlights.get("data", []):
            # Use the 'id' field if available, or fallback to 'url'
            item_key = record.get("id") or record.get("url")
            if item_key is None:
                # Skip records without a unique identifier
                continue

            # Convert the item key to a string if it's not already one.
            item_key = str(item_key)
            record["id"] = item_key  # Ensure the record's id field is a string

            # Optionally add the fetch date
            record["fetch_date"] = DATE

            table.put_item(Item=record)
            print(f"Stored record with key {item_key} into DynamoDB.")
    except Exception as e:
        print(f"Error storing highlights in DynamoDB: {e}")


def process_highlights():
    """
    Main function to fetch and process basketball highlights.
    """
    print("Fetching highlights...")
    highlights = fetch_highlights()
    if highlights:
        print("Saving highlights to S3...")
        save_to_s3(highlights, "basketball_highlights")
        print("Storing highlights in DynamoDB...")
        store_highlights_to_dynamodb(highlights)

if __name__ == "__main__":
    process_highlights()
