# ecs.tf

resource "aws_ecs_cluster" "this" {
  name = "${var.project_name}-cluster"
}

resource "aws_cloudwatch_log_group" "ecs_log_group" {
  name              = "/ecs/${var.project_name}"
  retention_in_days = 7
}

resource "aws_ecs_task_definition" "this" {
  family                   = "${var.project_name}-task"
  cpu                      = 256
  memory                   = 512
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = templatefile("${path.module}/container_definitions.tpl", {
    ecr_image_url              = "${aws_ecr_repository.this.repository_url}:latest"
    log_group_name             = aws_cloudwatch_log_group.ecs_log_group.name
    aws_region                 = var.aws_region
    bucket_name                = var.s3_bucket_name
    rapidapi_ssm_parameter_arn = var.rapidapi_ssm_parameter_arn
    mediaconvert_endpoint      = var.mediaconvert_endpoint
    mediaconvert_role_arn      = var.mediaconvert_role_arn
  })
}

resource "aws_ecs_service" "this" {
  name            = "${var.project_name}-service"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.this.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.public_subnets
    security_groups  = [aws_security_group.ecs_task.id]
    assign_public_ip = true
  }

  deployment_controller {
    type = "ECS"
  }

  tags = {
    Name = "${var.project_name}-service"
  }
}
