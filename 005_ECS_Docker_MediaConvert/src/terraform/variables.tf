# variables.tf

variable "environment" {
  description = "Deployment environment (e.g., dev, prod, staging)"
  type        = string
}

variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
}

variable "project_name" {
  description = "Name of the project"
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
variable "image_tag" {
  description = "Tag for building the image"
  type        = string
}

variable "mediaconvert_endpoint" {
  description = "AWS MediaConvert endpoint"
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
