# process_one_video.py

# Import the 'json' module for handling JSON data serialization and deserialization
import json

# Import the 'boto3' library for interacting with AWS services like S3
import boto3

# Import the 'requests' library for making HTTP requests to external URLs
import requests

# Import 'BytesIO' from the 'io' module to handle in-memory binary streams
from io import BytesIO

# Import specific configuration variables from the 'config.py' module
from config import (
    S3_BUCKET_NAME,  # The name of the Amazon S3 bucket used for input/output data
    AWS_REGION,      # The AWS region where the S3 bucket is located
    INPUT_KEY,       # The S3 key (path) for the input JSON file containing video URLs
    OUTPUT_KEY       # The S3 key (path) where the processed video will be saved
)

def process_one_video():
    """
    Fetch a highlight URL from the JSON file in S3, download the video,
    and save it back to S3.
    
    This function performs the following steps:
    1. Connects to the specified S3 bucket.
    2. Retrieves the input JSON file containing video URLs.
    3. Extracts the first video URL from the JSON data.
    4. Downloads the video from the extracted URL.
    5. Uploads the downloaded video to the specified S3 location.
    """
    try:
        # Initialize the S3 client with the specified AWS region
        s3 = boto3.client("s3", region_name=AWS_REGION)

        # Inform the user that the JSON file retrieval process has started
        print("Fetching JSON file from S3...")

        # Retrieve the JSON file from S3 using the specified bucket and key
        response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=INPUT_KEY)

        # Read the content of the retrieved object and decode it from bytes to a UTF-8 string
        json_content = response['Body'].read().decode('utf-8')

        # Parse the JSON string into a Python dictionary
        highlights = json.loads(json_content)

        # Extract the first video URL from the JSON data
        # Adjust the key path ('["data"][0]["url"]') based on the actual structure of your JSON
        video_url = highlights["data"][0]["url"]

        # Inform the user about the video URL being processed
        print(f"Processing video URL: {video_url}")

        # Inform the user that the video download process has started
        print("Downloading video...")

        # Make a GET request to the video URL to download the video content
        # 'stream=True' allows streaming the response content
        video_response = requests.get(video_url, stream=True)

        # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        video_response.raise_for_status()

        # Read the content of the video response and store it in a BytesIO object
        # This allows handling the video data in memory without saving it to disk
        video_data = BytesIO(video_response.content)

        # Inform the user that the video upload process has started
        print("Uploading video to S3...")

        # Upload the video data to S3 using the specified bucket and key
        s3.put_object(
            Bucket=S3_BUCKET_NAME,          # The target S3 bucket where the video will be stored
            Key=OUTPUT_KEY,                  # The S3 key (path) for the uploaded video
            Body=video_data,                 # The binary data of the video to upload
            ContentType="video/mp4"          # The MIME type of the uploaded file
        )

        # Inform the user that the video was uploaded successfully, including the S3 URL
        print(f"Video uploaded successfully: s3://{S3_BUCKET_NAME}/{OUTPUT_KEY}")

    except Exception as e:
        # Catch any exceptions that occur during the process and inform the user
        print(f"Error during video processing: {e}")

# Check if this script is being run as the main program
# If so, execute the 'process_one_video' function
if __name__ == "__main__":
    process_one_video()
