# mediaconvert_process.py
import json
import boto3

from config import (
    AWS_REGION,
    MEDIACONVERT_ENDPOINT,
    MEDIACONVERT_ROLE_ARN,
    S3_BUCKET_NAME
)

def create_job():
    """
    Create a MediaConvert job to process a video.
    """
    try:
        mediaconvert = boto3.client(
            "mediaconvert",
            region_name=AWS_REGION,
            endpoint_url=MEDIACONVERT_ENDPOINT
        )

        input_s3_url = f"s3://{S3_BUCKET_NAME}/videos/first_video.mp4"
        output_s3_url = f"s3://{S3_BUCKET_NAME}/processed_videos/"

        job_settings = {
            "Inputs": [
                {
                    "AudioSelectors": {
                        "Audio Selector 1": {"DefaultSelection": "DEFAULT"}
                    },
                    "FileInput": input_s3_url,
                    "VideoSelector": {}
                }
            ],
            "OutputGroups": [
                {
                    "Name": "File Group",
                    "OutputGroupSettings": {
                        "Type": "FILE_GROUP_SETTINGS",
                        "FileGroupSettings": {
                            "Destination": output_s3_url
                        }
                    },
                    "Outputs": [
                        {
                            "ContainerSettings": {
                                "Container": "MP4",
                                "Mp4Settings": {}
                            },
                            "VideoDescription": {
                                "CodecSettings": {
                                    "Codec": "H_264",
                                    "H264Settings": {
                                        "Bitrate": 5000000,
                                        "RateControlMode": "CBR",
                                        "QualityTuningLevel": "SINGLE_PASS",
                                        "CodecProfile": "MAIN"
                                    }
                                },
                                "ScalingBehavior": "DEFAULT",
                                "TimecodeInsertion": "DISABLED"
                            },
                            "AudioDescriptions": [
                                {
                                    "CodecSettings": {
                                        "Codec": "AAC",
                                        "AacSettings": {
                                            "Bitrate": 64000,
                                            "CodingMode": "CODING_MODE_2_0",
                                            "SampleRate": 48000
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        # Top-level parameters
        response = mediaconvert.create_job(
            Role=MEDIACONVERT_ROLE_ARN,
            Settings=job_settings,
            AccelerationSettings={"Mode": "DISABLED"},
            StatusUpdateInterval="SECONDS_60",
            Priority=0
        )

        print("MediaConvert job created successfully:")
        print(json.dumps(response, indent=4, default=str))

    except Exception as e:
        print(f"Error creating MediaConvert job: {e}")

if __name__ == "__main__":
    create_job()
