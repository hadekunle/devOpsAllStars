set -e

# AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
# AWS_REGION="us-east-1"
# REPO_NAME="highlight-processor"
# TAG='sports-api-latest'

AWS_ACCOUNT_ID=$1
AWS_REGION=$2
REPO_URL=$3
TAG=$4

aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $REPO_URL

docker build --platform linux/amd64 \
  -t $REPO_URL:$TAG ..
#   -t $REPO_NAME:$TAG \

# docker run --env-file ../.env $REPO_NAME

DOCKER_CLI_DEBUG=1 docker push $REPO_URL:$TAG > ../docker_push.log 2>&1