set -e

docker build -t highlight-processor .
docker run --env-file .env highlight-processor