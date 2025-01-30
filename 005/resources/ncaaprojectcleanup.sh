#!/bin/bash

# =====================================================================
# AWS Resources Cleanup Script
# =====================================================================
# This script deletes AWS ECS services and clusters, ECR repositories,
# Load Balancers, Security Groups, and CloudWatch Log Groups.
# It preserves S3 bucket contents and MediaConvert jobs.
# =====================================================================

# --------------------
# Variables (Customize these)
# --------------------
CLUSTER_NAME="highlight-pipeline-final-cluster"
ECR_REPO_NAME="highlight-pipeline2-final"
ALB_TAG_PREFIX="Project=highlight-pipeline-final"       # Tag to identify ALBs
SECURITY_GROUP_PREFIX="Project=highlight-pipeline-final" # Tag to identify Security Groups
LOG_GROUP_PREFIX="/ecs/highlight-pipeline-final"         # Prefix for CloudWatch Log Groups

# --------------------
# Function to delete ECS Services
# --------------------
delete_ecs_services() {
    echo "===== Deleting ECS Services in Cluster: $CLUSTER_NAME ====="
    SERVICES=$(aws ecs list-services --cluster "$CLUSTER_NAME" --query 'serviceArns' --output text)
    if [ -z "$SERVICES" ]; then
        echo "No ECS services found in cluster $CLUSTER_NAME."
    else
        for SERVICE in $SERVICES; do
            echo "Deleting ECS Service: $SERVICE"
            aws ecs delete-service --cluster "$CLUSTER_NAME" --service "$SERVICE" --force --region $(aws configure get region)
            echo "Waiting for service $SERVICE to be deleted..."
            aws ecs wait services-inactive --cluster "$CLUSTER_NAME" --services "$SERVICE" --region $(aws configure get region)
            echo "Service $SERVICE deleted."
        done
    fi
}

# --------------------
# Function to delete ECS Cluster
# --------------------
delete_ecs_cluster() {
    echo "===== Deleting ECS Cluster: $CLUSTER_NAME ====="
    aws ecs delete-cluster --cluster "$CLUSTER_NAME" --region $(aws configure get region)
    echo "ECS Cluster $CLUSTER_NAME deleted."
}

# --------------------
# Function to delete ECR Repository
# --------------------
delete_ecr_repository() {
    echo "===== Deleting ECR Repository: $ECR_REPO_NAME ====="
    REPO_URI=$(aws ecr describe-repositories --repository-names "$ECR_REPO_NAME" --query 'repositories[0].repositoryUri' --output text --region $(aws configure get region))
    if [ -z "$REPO_URI" ]; then
        echo "ECR Repository $ECR_REPO_NAME does not exist."
    else
        echo "Deleting ECR Repository: $REPO_URI"
        aws ecr delete-repository --repository-name "$ECR_REPO_NAME" --force --region $(aws configure get region)
        echo "ECR Repository $ECR_REPO_NAME deleted."
    fi
}

# --------------------
# Function to delete Load Balancers
# --------------------
delete_load_balancers() {
    echo "===== Deleting Application Load Balancers (ALBs) ====="
    ALB_ARNS=$(aws elbv2 describe-load-balancers --query "LoadBalancers[?contains(Tags[].Key, 'Project') && contains(Tags[].Value, 'highlight-pipeline-final')].LoadBalancerArn" --output text --region $(aws configure get region))
    if [ -z "$ALB_ARNS" ]; then
        echo "No ALBs found with tag prefix '$ALB_TAG_PREFIX'."
    else
        for ALB_ARN in $ALB_ARNS; do
            ALB_NAME=$(aws elbv2 describe-load-balancers --load-balancer-arns "$ALB_ARN" --query 'LoadBalancers[0].LoadBalancerName' --output text --region $(aws configure get region))
            echo "Deleting ALB: $ALB_NAME ($ALB_ARN)"
            aws elbv2 delete-load-balancer --load-balancer-arn "$ALB_ARN" --region $(aws configure get region)
            echo "Waiting for ALB $ALB_NAME to be deleted..."
            aws elbv2 wait load-balancer-deleted --load-balancer-arn "$ALB_ARN" --region $(aws configure get region)
            echo "ALB $ALB_NAME deleted."
        done
    fi
}

# --------------------
# Function to delete Security Groups
# --------------------
delete_security_groups() {
    echo "===== Deleting Security Groups ====="
    SG_IDS=$(aws ec2 describe-security-groups --filters "Name=tag:Project,Values=highlight-pipeline-final" --query 'SecurityGroups[*].GroupId' --output text --region $(aws configure get region))
    if [ -z "$SG_IDS" ]; then
        echo "No Security Groups found with tag prefix '$SECURITY_GROUP_PREFIX'."
    else
        for SG_ID in $SG_IDS; do
            SG_NAME=$(aws ec2 describe-security-groups --group-ids "$SG_ID" --query 'SecurityGroups[0].GroupName' --output text --region $(aws configure get region))
            echo "Deleting Security Group: $SG_NAME ($SG_ID)"
            aws ec2 delete-security-group --group-id "$SG_ID" --region $(aws configure get region)
            echo "Security Group $SG_NAME deleted."
        done
    fi
}

# --------------------
# Function to delete CloudWatch Log Groups
# --------------------
delete_log_groups() {
    echo "===== Deleting CloudWatch Log Groups ====="
    LOG_GROUPS=$(aws logs describe-log-groups --log-group-name-prefix "$LOG_GROUP_PREFIX" --query 'logGroups[*].logGroupName' --output text --region $(aws configure get region))
    if [ -z "$LOG_GROUPS" ]; then
        echo "No CloudWatch Log Groups found with prefix '$LOG_GROUP_PREFIX'."
    else
        for LOG_GROUP in $LOG_GROUPS; do
            echo "Deleting Log Group: $LOG_GROUP"
            aws logs delete-log-group --log-group-name "$LOG_GROUP" --region $(aws configure get region)
            echo "Log Group $LOG_GROUP deleted."
        done
    fi
}

# --------------------
# Main Execution
# --------------------
echo "===== Starting AWS Resources Cleanup ====="
delete_ecs_services
delete_ecs_cluster
delete_ecr_repository
delete_load_balancers
delete_security_groups
delete_log_groups
echo "===== AWS Resources Cleanup Completed ====="
