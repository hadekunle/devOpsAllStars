provider "aws" {
  region = "us-east-1"
}

# SNS Topic
resource "aws_sns_topic" "nba_game_alerts" {
  name = "nba_game_alerts"
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "nba_lambda_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

# IAM Policy for Lambda to publish to SNS
resource "aws_iam_policy" "sns_publish_policy" {
  name        = "sns_publish_policy"
  description = "Policy to allow Lambda to publish to SNS"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sns:Publish",
      "Resource": "${aws_sns_topic.nba_game_alerts.arn}"
    }
  ]
}
EOF
}

# Attach IAM Policy for Lambda to publish to SNS to IAM Role
resource "aws_iam_role_policy_attachment" "attach_sns_publish" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.sns_publish_policy.arn
}


data "aws_caller_identity" "current" {}

# IAM Policy to Read From Parameter Store
resource "aws_iam_policy" "ssm_policy" {
  name        = "ssm_parameter_access"
  description = "Allow Lambda to read NBA API Key from Parameter Store"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ssm:GetParameter",
      "Resource": "arn:aws:ssm:us-east-1:${data.aws_caller_identity.current.account_id}:parameter/nba-api-key"
    }
  ]
}
EOF
}

# Attach IAM Policy to Read From Parameter Store to IAM Role
resource "aws_iam_role_policy_attachment" "attach_read_param_store" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.ssm_policy.arn
}


# IAM Policy for CloudWatch Logs (Lambda Execution)
resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging_policy"
  description = "Allow Lambda to write logs"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
EOF
}

# Attach CloudWatch Logging Policy to IAM Role
resource "aws_iam_role_policy_attachment" "attach_logging" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

# Lambda Function
resource "aws_lambda_function" "nba_lambda" {
  filename      = "nba_notifications.zip" # Pre-packaged ZIP
  function_name = "nba_game_alerts"
  role          = aws_iam_role.lambda_role.arn
  handler       = "nba_notifications.lambda_handler"
  runtime       = "python3.8"

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.nba_game_alerts.arn
    }
  }
}

# EventBridge Rule for Scheduling
resource "aws_cloudwatch_event_rule" "nba_schedule" {
  name                = "nba_game_alerts_schedule"
  schedule_expression = "rate(2 hours)" # Adjust as needed
}

# EventBridge Target
resource "aws_cloudwatch_event_target" "nba_target" {
  rule      = aws_cloudwatch_event_rule.nba_schedule.name
  target_id = "nba_lambda"
  arn       = aws_lambda_function.nba_lambda.arn
}

# Grant EventBridge Permission to Invoke Lambda
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.nba_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.nba_schedule.arn
}
