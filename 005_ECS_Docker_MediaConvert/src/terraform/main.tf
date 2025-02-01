# main.tf

terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  # If you're storing Terraform state in S3, configure a backend block here.
  # Otherwise, local state is used by default.
  # backend "s3" {
  #   bucket  = "my-tf-state-bucket"
  #   key     = "highlight-pipeline/terraform.tfstate"
  #   region  = var.aws_region
  # }
}

# Optional local reference for your AWS account ID
locals {
  current_account_id = data.aws_caller_identity.current.account_id
}
