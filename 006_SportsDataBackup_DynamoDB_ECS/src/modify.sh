set -a
source .env
set +a

echo $AWS_LOGS_GROUP
echo $TASK_FAMILY

envsubst < taskdef.template.json > taskdef.json
envsubst < s3_dynamodb_policy.template.json > s3_dynamodb_policy.json
envsubst < ecsTarget.template.json > ecsTarget.json
envsubst < ecseventsrole-policy.template.json > ecseventsrole-policy.json
