# process_videos.py
import json
import boto3
import requests
from io import BytesIO

from config import (
    S3_BUCKET_NAME,
    AWS_REGION,
    INPUT_KEY,
    OUTPUT_KEY_PREFIX  # Changed from OUTPUT_KEY to a prefix for multiple videos
)

def process_videos():
    """
    Fetch the highlights JSON file from S3, iterate over all video URLs, download each video,
    and upload them back to S3.
    """
    try:
        s3 = boto3.client("s3", region_name=AWS_REGION)

        # Retrieve the JSON file from S3
        print("Fetching JSON file from S3...")
        response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=INPUT_KEY)
        json_content = response['Body'].read().decode('utf-8')
        highlights = json.loads(json_content)

        # Process each highlight record that has a video URL.
        videos = highlights.get("data", [])
        if not videos:
            print("No video records found in the JSON file.")
            return

        for index, record in enumerate(videos):
            video_url = record.get("url")
            if not video_url:
                print(f"Record {index} does not contain a video URL. Skipping.")
                continue

            print(f"Processing video URL {index}: {video_url}")

            # Download the video
            print("Downloading video...")
            video_response = requests.get(video_url, stream=True)
            video_response.raise_for_status()

            # Prepare the video data (BytesIO is optional here; you can use video_response.content directly)
            video_data = BytesIO(video_response.content)

            # Create a unique key for each video (e.g., videos/highlight_0.mp4, videos/highlight_1.mp4, etc.)
            output_key = f"{OUTPUT_KEY_PREFIX}highlight_{index}.mp4"

            # Upload the video to S3
            print(f"Uploading video to S3 with key: {output_key}...")
            s3.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=output_key,
                Body=video_data.getvalue(),
                ContentType="video/mp4"
            )
            print(f"Video uploaded successfully: s3://{S3_BUCKET_NAME}/{output_key}")

    except Exception as e:
        print(f"Error during video processing: {e}")

if __name__ == "__main__":
    process_videos()
