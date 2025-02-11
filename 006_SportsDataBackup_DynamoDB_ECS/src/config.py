# config.py
import os
from datetime import datetime

###################################
# RapidAPI & Fetch-Related Config
###################################
API_URL = os.getenv("API_URL", "https://sport-highlights-api.p.rapidapi.com/basketball/highlights")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "sport-highlights-api.p.rapidapi.com")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")  # No default, must be set at runtime

# Use the current day in YYYY-MM-DD format as the default date
DATE = os.getenv("DATE", datetime.utcnow().strftime("%Y-%m-%d"))
LEAGUE_NAME = os.getenv("LEAGUE_NAME", "NCAA")
LIMIT = int(os.getenv("LIMIT", "10"))

###################################
# AWS & S3
###################################
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

###################################
# DynamoDB
###################################
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "SportsHighlights")

###################################
# MediaConvert
###################################
MEDIACONVERT_ENDPOINT = os.getenv("MEDIACONVERT_ENDPOINT")
MEDIACONVERT_ROLE_ARN = os.getenv("MEDIACONVERT_ROLE_ARN")

###################################
# Video Paths in S3
###################################
INPUT_KEY = os.getenv("INPUT_KEY", "highlights/basketball_highlights.json")
# Note: For multiple videos, you may want to use a key pattern rather than a fixed name.
OUTPUT_KEY_PREFIX = os.getenv("OUTPUT_KEY_PREFIX", "videos/")

###################################
# run_all.py Retry/Delay Config
###################################
RETRY_COUNT = int(os.getenv("RETRY_COUNT", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "30"))
WAIT_TIME_BETWEEN_SCRIPTS = int(os.getenv("WAIT_TIME_BETWEEN_SCRIPTS", "60"))
