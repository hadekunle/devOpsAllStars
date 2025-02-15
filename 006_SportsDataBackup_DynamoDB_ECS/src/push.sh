set -a
source .env
set +a

echo $AWS_LOGS_GROUP
echo $TASK_FAMILY

# 1. Create an ECR Repo
aws ecr create-repository --repository-name sports-backup | cat
# 2.Log In To ECR
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
# 3. Build the Docker Image
docker build -t sports-backup .
# 4.Tag the Image for ECR
docker tag sports-backup:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/sports-backup:latest
# 5. Push the Image
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/sports-backup:latest

# sleep 300

#run ecs task manually
# aws ecs run-task \
#   --cluster sports-backup-cluster \
#   --launch-type FARGATE \
#   --task-definition ${TASK_FAMILY} \
#   --network-configuration "awsvpcConfiguration={subnets=[\"${SUBNET_ID}\"],securityGroups=[\"${SECURITY_GROUP_ID}\"],assignPublicIp=\"ENABLED\"}" \
#   --region ${AWS_REGION} | cat