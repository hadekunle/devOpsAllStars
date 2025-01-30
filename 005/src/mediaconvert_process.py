# mediaconvert_process.py

# Import the 'json' module for handling JSON data serialization and deserialization
import json

# Import the 'boto3' library for interacting with AWS services like MediaConvert and S3
import boto3

# Import specific configuration variables from the 'config.py' module
from config import (
    AWS_REGION,               # AWS region where services are deployed (e.g., 'us-east-1')
    MEDIACONVERT_ENDPOINT,    # The endpoint URL for AWS MediaConvert service
    MEDIACONVERT_ROLE_ARN,    # The Amazon Resource Name (ARN) for the IAM role used by MediaConvert
    S3_BUCKET_NAME            # The name of the Amazon S3 bucket used for input/output data
)

def create_job():
    """
    Create a MediaConvert job to process a video.
    
    This function initializes the MediaConvert client, defines the job settings,
    and submits a job to AWS MediaConvert for processing a video file stored in S3.
    """
    try:
        # Initialize the MediaConvert client with specified region and endpoint
        mediaconvert = boto3.client(
            "mediaconvert",                    # AWS MediaConvert service
            region_name=AWS_REGION,            # AWS region from configuration
            endpoint_url=MEDIACONVERT_ENDPOINT  # MediaConvert endpoint URL from configuration
        )

        # Define the S3 URL for the input video file to be processed
        input_s3_url = f"s3://{S3_BUCKET_NAME}/videos/first_video.mp4"

        # Define the S3 URL where the processed videos will be saved
        output_s3_url = f"s3://{S3_BUCKET_NAME}/processed_videos/"

        # Define the job settings for MediaConvert
        job_settings = {
            "Inputs": [  # List of input sources for the MediaConvert job
                {
                    "AudioSelectors": {  # Define audio selection settings
                        "Audio Selector 1": {"DefaultSelection": "DEFAULT"}  # Select default audio track
                    },
                    "FileInput": input_s3_url,  # Specify the input video file S3 URL
                    "VideoSelector": {}         # Video selection settings (empty means default)
                }
            ],
            "OutputGroups": [  # Define output group settings
                {
                    "Name": "File Group",  # Name identifier for the output group
                    "OutputGroupSettings": {  # Settings specific to the output group
                        "Type": "FILE_GROUP_SETTINGS",  # Type of output group
                        "FileGroupSettings": {  # Settings related to file group outputs
                            "Destination": output_s3_url  # S3 destination URL for processed videos
                        }
                    },
                    "Outputs": [  # List of output configurations within the output group
                        {
                            "ContainerSettings": {  # Container format settings
                                "Container": "MP4",       # Output container format (MP4)
                                "Mp4Settings": {}         # Additional MP4-specific settings (empty for defaults)
                            },
                            "VideoDescription": {  # Description of video settings
                                "CodecSettings": {  # Codec configuration for video
                                    "Codec": "H_264",  # Video codec to use (H.264)
                                    "H264Settings": {  # Specific settings for H.264 codec
                                        "Bitrate": 5000000,              # Bitrate in bits per second
                                        "RateControlMode": "CBR",        # Constant Bit Rate control mode
                                        "QualityTuningLevel": "SINGLE_PASS",  # Quality tuning level
                                        "CodecProfile": "MAIN"            # H.264 codec profile
                                    }
                                },
                                "ScalingBehavior": "DEFAULT",  # Behavior for scaling video resolution
                                "TimecodeInsertion": "DISABLED"  # Disable timecode insertion
                            },
                            "AudioDescriptions": [  # List of audio configurations
                                {
                                    "CodecSettings": {  # Codec configuration for audio
                                        "Codec": "AAC",  # Audio codec to use (AAC)
                                        "AacSettings": {  # Specific settings for AAC codec
                                            "Bitrate": 64000,           # Bitrate in bits per second
                                            "CodingMode": "CODING_MODE_2_0",  # Audio coding mode (2.0 channels)
                                            "SampleRate": 48000        # Audio sample rate in Hz
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        # Submit the MediaConvert job with the defined settings and additional parameters
        response = mediaconvert.create_job(
            Role=MEDIACONVERT_ROLE_ARN,                 # IAM role ARN that MediaConvert assumes
            Settings=job_settings,                      # Job settings defined above
            AccelerationSettings={"Mode": "DISABLED"},  # Disable acceleration settings
            StatusUpdateInterval="SECONDS_60",           # Interval for status updates (every 60 seconds)
            Priority=0                                   # Priority of the job (0 is default)
        )

        # Print a success message indicating the job was created
        print("MediaConvert job created successfully:")

        # Pretty-print the JSON response from MediaConvert
        print(json.dumps(response, indent=4))

    except Exception as e:
        # Catch any exceptions that occur during job creation and print an error message
        print(f"Error creating MediaConvert job: {e}")

# Check if this script is being run as the main program
if __name__ == "__main__":
    # Call the 'create_job' function to initiate the MediaConvert job
    create_job()
