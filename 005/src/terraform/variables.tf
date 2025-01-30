# variables.tf

variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
}

variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "environment" {
  description = "Deployment environment (e.g., dev, prod, staging)"
  type        = string
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket for storing highlights"
  type        = string
}

variable "ecr_repository_name" {
  description = "Name of the ECR repository"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "public_subnets" {
  description = "List of public subnet IDs"
  type        = list(string)
}

variable "private_subnets" {
  description = "List of private subnet IDs"
  type        = list(string)
}

variable "igw_id" {
  description = "Internet Gateway ID"
  type        = string
}

variable "public_route_table_id" {
  description = "Public Route Table ID"
  type        = string
}

variable "private_route_table_id" {
  description = "Private Route Table ID"
  type        = string
}

variable "rapidapi_ssm_parameter_arn" {
  description = "ARN of the RapidAPI key stored in SSM Parameter Store"
  type        = string
}

variable "mediaconvert_endpoint" {
  description = "AWS MediaConvert endpoint"
  type        = string
}

variable "mediaconvert_role_arn" {
  description = "ARN of the MediaConvert IAM role"
  type        = string
}

variable "retry_count" {
  description = "Number of retry attempts for failed operations"
  type        = number
  default     = 5
}

variable "retry_delay" {
  description = "Delay in seconds between retry attempts"
  type        = number
  default     = 60
}
