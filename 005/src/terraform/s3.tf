resource "aws_s3_bucket" "highlights" {
  bucket = var.s3_bucket_name
  # Enable versioning or encryption if needed
  # versioning {
  #   enabled = true
  # }
  # server_side_encryption_configuration {
  #   rule {
  #     apply_server_side_encryption_by_default {
  #       sse_algorithm = "AES256"
  #     }
  #   }
  # }
}
