set -e 
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
AWS_REGION="us-east-1"
REPO_NAME="sports-api"

aws ecr create-repository --repository-name $REPO_NAME --region $AWS_REGION
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME

sleep 2
docker build --platform linux/amd64 \
  -t $REPO_NAME:latest \
  -t $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:latest .

sleep 2
DOCKER_CLI_DEBUG=1 docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:latest > docker_push.log 2>&1