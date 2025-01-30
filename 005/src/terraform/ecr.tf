resource "aws_ecr_repository" "this" {
  name                 = var.ecr_repository_name
  image_tag_mutability = "MUTABLE"
}
