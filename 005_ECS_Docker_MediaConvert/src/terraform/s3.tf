# resource "aws_s3_bucket" "highlights" {
#   bucket = var.s3_bucket_name
#   # force_destroy = false

#   lifecycle {
#     prevent_destroy = true
#   }
# }

data "aws_s3_bucket" "highlights" {
  bucket = var.s3_bucket_name
}

resource "aws_s3_bucket_policy" "highlight_policy" {
  bucket = data.aws_s3_bucket.highlights.id
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${aws_iam_role.mediaconvert_role.name}",
                    "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${aws_iam_role.ecs_task_execution_role.name}"
                ]
            },
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::${var.s3_bucket_name}/*"
        }
    ]
}
  EOF
}