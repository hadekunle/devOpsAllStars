# iam.tf

# Retrieve AWS account information
data "aws_caller_identity" "current" {}

# Define the trust relationship for ECS tasks
data "aws_iam_policy_document" "ecs_task_trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"] #For eventBridge permissions
    }
  }
}

# Create the ECS task execution role
resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "${var.project_name}-ecs-task-execution-role-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_trust.json

  tags = {
    env = "${var.environment}"
  }
}

# Attach the AWS-managed ECS Task Execution policy
resource "aws_iam_role_policy_attachment" "ecs_task_execution_attach" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"

}

# Define the custom IAM policy document
data "aws_iam_policy_document" "ecs_custom_doc" {
  # statement {
  #   actions   = ["*"]
  #   effect    = "Allow"
  #   resources = ["*"]
  # }

  version = "2012-10-17"
  #TODO: reduce permissions on roles
  # 1) S3 Permissions
  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:ListBucket"
    ]
    effect = "Allow"
    resources = [
      "arn:aws:s3:::${var.s3_bucket_name}",  # Bucket-level permissions
      "arn:aws:s3:::${var.s3_bucket_name}/*" # Object-level permissions
    ]
  }

  # 2) SSM Parameter Store Permissions
  statement {
    actions = [
      "ssm:GetParameter",
      "ssm:GetParameters",
      "ssm:GetParameterHistory"
    ]
    effect = "Allow"
    resources = [
      "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter/${data.aws_ssm_parameter.rapidapi_ssm_parameter.name}"
    ]
  }

  # 3) MediaConvert Permissions
  statement {
    actions = [
      "mediaconvert:CreateJob",
      "mediaconvert:GetJob",
      "mediaconvert:ListJobs"
    ]
    effect    = "Allow"
    resources = ["*"] # MediaConvert requires "*" for resource ARN
  }

  # 4) Add IAM Passrole
  statement {
    actions = [
      "iam:PassRole"
    ]
    effect = "Allow"
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${aws_iam_role.ecs_task_execution_role.name}"
    ]
  }

  # 5) Add permissions to run ECS tasks
  statement {
    actions = [
      "ecs:RunTask"
    ]
    effect = "Allow"
    resources = [
      "arn:aws:ecs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:task-definition/${aws_ecs_task_definition.this.family}:*",
    ]
    # TODO: add conditions later
    #   condition {
    #     test     = "ArnEquals"
    #     variable = "ecs:cluster"
    #     values   = ["arn:aws:ecs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:cluster/${aws_ecs_cluster.this.name}"]
    #   }
  }
}

# Create the custom IAM policy
resource "aws_iam_policy" "ecs_custom_policy" {
  name   = "${var.project_name}-ecs-custom-policy-${var.environment}"
  policy = data.aws_iam_policy_document.ecs_custom_doc.json
}

# Attach the custom IAM policy to the ECS task execution role
resource "aws_iam_role_policy_attachment" "ecs_custom_attach" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.ecs_custom_policy.arn
}

# Define the trust relationship for MediaConvert
data "aws_iam_policy_document" "mediaconvert_trust" {
  version = "2012-10-17"
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["mediaconvert.amazonaws.com"]
    }
  }
}

# Create the MediaConvert role
resource "aws_iam_role" "mediaconvert_role" {
  name               = "${var.project_name}-mediaconvert-role-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.mediaconvert_trust.json
  tags = {
    env = "${var.environment}"
  }
}

# Define the MediaConvert policy document
data "aws_iam_policy_document" "mediaconvert_policy_doc" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject"
    ]
    effect    = "Allow"
    resources = ["arn:aws:s3:::${var.s3_bucket_name}/*"]
  }
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    effect    = "Allow"
    resources = ["arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/ecs/${var.project_name}/*"]
  }
}

# Create the MediaConvert policy
resource "aws_iam_policy" "mediaconvert_policy" {
  name   = "${var.project_name}-mediaconvert-s3-logs-${var.environment}"
  policy = data.aws_iam_policy_document.mediaconvert_policy_doc.json
}

# Attach the MediaConvert policy to the MediaConvert role
resource "aws_iam_role_policy_attachment" "mediaconvert_attach" {
  role       = aws_iam_role.mediaconvert_role.name
  policy_arn = aws_iam_policy.mediaconvert_policy.arn
}
