# config.py

# Import the 'os' module to access environment variables
import os

###################################
# RapidAPI & Fetch-Related Config
###################################

# The base URL for the sports highlights API. 
# If the 'API_URL' environment variable is not set, it defaults to the provided URL.
API_URL = os.getenv("API_URL", "https://sport-highlights-api.p.rapidapi.com/basketball/highlights")

# The host for the RapidAPI service. 
# If the 'RAPIDAPI_HOST' environment variable is not set, it defaults to the provided host.
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "sport-highlights-api.p.rapidapi.com")
# The API key for authenticating with RapidAPI.
# No default is provided, so the application will fail at runtime if 'RAPIDAPI_KEY' is not set.
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# The date for which to fetch basketball highlights. 
# If the 'DATE' environment variable is not set, it defaults to '2023-12-01'.
DATE = os.getenv("DATE", "2023-12-01")

# The name of the basketball league. 
# If the 'LEAGUE_NAME' environment variable is not set, it defaults to 'NCAA'.
LEAGUE_NAME = os.getenv("LEAGUE_NAME", "NCAA")

# The maximum number of highlights to fetch. 
# It converts the 'LIMIT' environment variable to an integer, defaulting to 10 if not set.
LIMIT = int(os.getenv("LIMIT", "10"))

###################################
# AWS & S3
###################################

# The name of the Amazon S3 bucket where data will be stored. 
# This must be set via the 'S3_BUCKET_NAME' environment variable.
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# The AWS region where resources are deployed. 
# If the 'AWS_REGION' environment variable is not set, it defaults to 'us-east-1'.
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

###################################
# MediaConvert
###################################

# The endpoint URL for AWS MediaConvert service. 
# If the 'MEDIACONVERT_ENDPOINT' environment variable is not set, it remains 'None'.
MEDIACONVERT_ENDPOINT = os.getenv("MEDIACONVERT_ENDPOINT")

# The Amazon Resource Name (ARN) for the IAM role used by MediaConvert. 
# It must be set via the 'MEDIACONVERT_ROLE_ARN' environment variable.
# Using the full ARN allows for more precise permissions and avoids hard-coding the account ID.
MEDIACONVERT_ROLE_ARN = os.getenv("MEDIACONVERT_ROLE_ARN")

###################################
# Video Paths in S3
###################################

# The key (path) in the S3 bucket where input highlights JSON file is stored.
# If the 'INPUT_KEY' environment variable is not set, it defaults to 'highlights/basketball_highlights.json'.
INPUT_KEY = os.getenv("INPUT_KEY", "highlights/basketball_highlights.json")

# The key (path) in the S3 bucket where the output processed video will be stored.
# If the 'OUTPUT_KEY' environment variable is not set, it defaults to 'videos/first_video.mp4'.
OUTPUT_KEY = os.getenv("OUTPUT_KEY", "videos/first_video.mp4")

###################################
# run_all.py Retry/Delay Config
###################################

# The number of times to retry a failed operation. 
# It converts the 'RETRY_COUNT' environment variable to an integer, defaulting to 3 if not set.
RETRY_COUNT = int(os.getenv("RETRY_COUNT", "3"))

# The delay (in seconds) between retry attempts. 
# It converts the 'RETRY_DELAY' environment variable to an integer, defaulting to 30 seconds if not set.
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "30"))

# The waiting time (in seconds) between the execution of different scripts within the pipeline.
# It converts the 'WAIT_TIME_BETWEEN_SCRIPTS' environment variable to an integer, defaulting to 60 seconds if not set.
WAIT_TIME_BETWEEN_SCRIPTS = int(os.getenv("WAIT_TIME_BETWEEN_SCRIPTS", "60"))
