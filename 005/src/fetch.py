# fetch.py

# Import the 'json' module for handling JSON data
import json

# Import the 'boto3' library for interacting with AWS services like S3
import boto3

# Import the 'requests' library for making HTTP requests to external APIs
import requests

# Import specific configuration variables from the 'config.py' module
from config import (
    API_URL,             # The endpoint URL for fetching sports highlights
    RAPIDAPI_HOST,       # The host for the RapidAPI service
    RAPIDAPI_KEY,        # The API key for authenticating with RapidAPI
    DATE,                # The date for which to fetch highlights
    LEAGUE_NAME,         # The name of the basketball league (e.g., NCAA)
    LIMIT,               # The maximum number of highlights to fetch
    S3_BUCKET_NAME,      # The name of the S3 bucket where data will be stored
    AWS_REGION,          # The AWS region where the S3 bucket is located
)

def fetch_highlights():
    """
    Fetch basketball highlights from the API.
    
    This function makes a GET request to the specified API endpoint with the necessary
    headers and query parameters to retrieve basketball highlights. It handles any
    request-related exceptions and returns the fetched highlights as a JSON object.
    
    Returns:
        dict or None: The fetched highlights as a JSON dictionary if successful; otherwise, None.
    """
    try:
        # Define the query parameters for the API request
        query_params = {
            "date": DATE,            # The specific date for which to fetch highlights
            "leagueName": LEAGUE_NAME,  # The name of the league (e.g., NCAA)
            "limit": LIMIT            # The maximum number of highlights to retrieve
        }
        
        # Define the headers for the API request, including authentication details
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,      # API key for RapidAPI authentication
            "X-RapidAPI-Host": RAPIDAPI_HOST     # Hostname for the RapidAPI service
        }

        # Make a GET request to the API endpoint with the specified headers and query parameters
        # Set a timeout of 120 seconds to prevent hanging requests
        response = requests.get(API_URL, headers=headers, params=query_params, timeout=120)
        
        # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()
        
        # Parse the JSON response from the API
        highlights = response.json()
        
        # Print a success message to indicate that highlights were fetched successfully
        print("Highlights fetched successfully!")
        
        # Return the parsed highlights data
        return highlights

    except requests.exceptions.RequestException as e:
        # Catch any exceptions related to the HTTP request and print an error message
        print(f"Error fetching highlights: {e}")
        
        # Return None to indicate that fetching highlights failed
        return None

def save_to_s3(data, file_name):
    """
    Save data to an S3 bucket.
    
    This function uploads the provided data to a specified S3 bucket. It first checks
    whether the bucket exists and creates it if it does not. The data is then serialized
    to JSON and uploaded to the S3 bucket with the specified file name.
    
    Args:
        data (dict): The data to be saved to S3.
        file_name (str): The name of the file (without extension) to be created in S3.
    """
    try:
        # Initialize the S3 client using the specified AWS region
        s3 = boto3.client("s3", region_name=AWS_REGION)

        # Attempt to check if the specified S3 bucket exists by calling 'head_bucket'
        try:
            s3.head_bucket(Bucket=S3_BUCKET_NAME)
            # If the bucket exists, print a confirmation message
            print(f"Bucket {S3_BUCKET_NAME} exists.")
        except Exception:
            # If the bucket does not exist, print a message indicating creation
            print(f"Bucket {S3_BUCKET_NAME} does not exist. Creating...")
            if AWS_REGION == "us-east-1":
                # For the 'us-east-1' region, the 'LocationConstraint' is not required
                s3.create_bucket(Bucket=S3_BUCKET_NAME)
            else:
                # For other regions, specify the 'LocationConstraint' during bucket creation
                s3.create_bucket(
                    Bucket=S3_BUCKET_NAME,
                    CreateBucketConfiguration={"LocationConstraint": AWS_REGION}
                )
            # Print a success message after creating the bucket
            print(f"Bucket {S3_BUCKET_NAME} created successfully.")

        # Define the S3 key (path) where the JSON data will be stored
        s3_key = f"highlights/{file_name}.json"

        # Upload the JSON data to the specified S3 bucket and key
        s3.put_object(
            Bucket=S3_BUCKET_NAME,                     # The target S3 bucket
            Key=s3_key,                                # The S3 key (path) for the uploaded file
            Body=json.dumps(data),                      # The JSON-serialized data to upload
            ContentType="application/json"             # The MIME type of the uploaded file
        )
        
        # Print a success message indicating where the data was saved in S3
        print(f"Highlights saved to S3: s3://{S3_BUCKET_NAME}/{s3_key}")
    
    except Exception as e:
        # Catch any exceptions related to S3 operations and print an error message
        print(f"Error saving to S3: {e}")

def process_highlights():
    """
    Main function to fetch and process basketball highlights.
    
    This function orchestrates the workflow of fetching basketball highlights from the API
    and saving them to an S3 bucket. It first calls 'fetch_highlights' to retrieve the data,
    and if successful, proceeds to call 'save_to_s3' to store the data in S3.
    """
    # Print a message indicating the start of the highlights fetching process
    print("Fetching highlights...")
    
    # Call the 'fetch_highlights' function to retrieve highlights data from the API
    highlights = fetch_highlights()
    
    # Check if highlights were successfully fetched
    if highlights:
        # Print a message indicating the start of the S3 saving process
        print("Saving highlights to S3...")
        
        # Call the 'save_to_s3' function to upload the fetched highlights to S3
        save_to_s3(highlights, "basketball_highlights")

# Check if this script is being run as the main program
# If so, execute the 'process_highlights' function
if __name__ == "__main__":
    process_highlights()
