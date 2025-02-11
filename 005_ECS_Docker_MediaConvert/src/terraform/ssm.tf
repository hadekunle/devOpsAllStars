# resource "aws_ssm_parameter" "rapidapi_ssm_parameter" {
#   name  = "rapid_api_key"
#   type  = "String"
#   value = "xxxxx"
# }

# Initially created with ssm resource above then removed from state file and read via data block below

data "aws_ssm_parameter" "rapidapi_ssm_parameter" {
  name = "rapid_api_key"
}

#TODO: enable secrets and it's rotation
# resource "aws_secretsmanager_secret_rotation" "example" {
#   secret_id           = aws_secretsmanager_secret.example.id
#   rotation_lambda_arn = aws_lambda_function.example.arn

#   rotation_rules {
#     automatically_after_days = 30
#   }
# }