# ecs.tf

resource "aws_ecs_cluster" "this" {
  name = "${var.project_name}-cluster-${var.environment}"
  tags = {
    env = "${var.environment}"
  }
}

resource "aws_cloudwatch_log_group" "ecs_log_group" {
  name              = "/ecs/${var.project_name}-${var.environment}"
  retention_in_days = 7
  tags = {
    env = "${var.environment}"
  }
}

resource "aws_ecs_task_definition" "this" {
  family                   = "${var.project_name}-task-${var.environment}"
  cpu                      = 256 #4096
  memory                   = 512 #8192
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = templatefile("${path.module}/container_definitions.tpl", {
    task_name      = var.project_name
    ecr_image_url  = "${data.aws_ecr_repository.this.repository_url}:${var.image_tag}"
    log_group_name = aws_cloudwatch_log_group.ecs_log_group.name
    aws_region     = var.aws_region
    bucket_name    = var.s3_bucket_name
    # rapidapi_ssm_parameter_arn = var.rapidapi_ssm_parameter_arn
    rapidapi_ssm_parameter_arn = data.aws_ssm_parameter.rapidapi_ssm_parameter.arn
    mediaconvert_endpoint      = var.mediaconvert_endpoint
    mediaconvert_role_arn      = aws_iam_role.mediaconvert_role.name
  })

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  tags = {
    env  = "${var.environment}"
  }
  
  depends_on = [data.aws_ssm_parameter.rapidapi_ssm_parameter]
}

# data "aws_ecs_task_execution" "example" {
#   cluster         = aws_ecs_cluster.this.arn
#   task_definition = aws_ecs_task_definition.this.arn
#   desired_count   = 1
#   launch_type     = "FARGATE"

#   network_configuration {
#     subnets          = [aws_subnet.public.id]
#     security_groups  = [aws_security_group.ecs_task.id]
#     assign_public_ip = true
#   }
# }


# resource "null_resource" "run_ecs_task" {
#   triggers = {
#     task_run_id = timestamp()
#   }
#   provisioner "local-exec" {
#     command = <<EOT
#       aws ecs run-task \
#         --cluster ${aws_ecs_cluster.this.id} \
#         --task-definition ${aws_ecs_task_definition.this.family} \
#         --launch-type FARGATE \
#         --network-configuration "awsvpcConfiguration={subnets=[\"${aws_subnet.public.id}\"],securityGroups=[\"${aws_security_group.ecs_task.id}\"],assignPublicIp=\"ENABLED\"}"
#     EOT
#   }

#   depends_on = [aws_ecs_task_definition.this, aws_ecs_cluster.this, null_resource.docker_build_push]
# }




# resource "aws_ecs_service" "this" {
#   name            = "${var.project_name}-service"
#   cluster         = aws_ecs_cluster.this.id
#   task_definition = aws_ecs_task_definition.this.arn
#   desired_count   = 1
#   launch_type = "FARGATE"

#   deployment_minimum_healthy_percent = 0
#   deployment_maximum_percent         = 100

#   network_configuration {
#     subnets          = [aws_subnet.public.id]
#     security_groups  = [aws_security_group.ecs_task.id]
#     assign_public_ip = false
#   }

#   deployment_controller {
#     type = "ECS"
#   }

#   tags = {
#     name = "${var.project_name}-service"
#     env  = "${var.environment}"

#   }
# }
