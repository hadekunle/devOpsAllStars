resource "aws_cloudwatch_event_rule" "ecs_run_schedule" {
  name                = "run-ecs-task-schedule-${var.environment}"
  description         = "EventBridge Rule to run tasks"
  schedule_expression = "rate(3 minutes)"
  # schedule_expression = "cron(0/2 * 9 2 ? 2025)"
  # schedule_expression = "cron(MIN HOUR DAY MONTH ? YEAR)" time has to be in UTC timezone
  tags = {
    env = "${var.environment}"
  }
}


resource "aws_cloudwatch_event_target" "ecs_task_target" {
  arn      = aws_ecs_cluster.this.arn
  rule     = aws_cloudwatch_event_rule.ecs_run_schedule.name
  role_arn = aws_iam_role.ecs_task_execution_role.arn

  ecs_target {
    task_definition_arn = aws_ecs_task_definition.this.arn
    launch_type         = "FARGATE"

    network_configuration {
      subnets          = [aws_subnet.public.id]
      security_groups  = [aws_security_group.ecs_task.id]
      assign_public_ip = true
    }
  }

}
