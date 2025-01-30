[
  {
    "name": "highlight-pipeline",
    "image": "${ecr_image_url}",
    "essential": true,
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-region": "${aws_region}",
        "awslogs-group": "${log_group_name}",
        "awslogs-stream-prefix": "ecs"
      }
    },
    "environment": [
      {
        "name": "AWS_REGION",
        "value": "${aws_region}"
      },
      {
        "name": "S3_BUCKET_NAME",
        "value": "${bucket_name}"
      },
      {
        "name": "MEDIACONVERT_ENDPOINT",
        "value": "${mediaconvert_endpoint}"
      },
      {
        "name": "MEDIACONVERT_ROLE_ARN",
        "value": "${mediaconvert_role_arn}"
      }
    ],
    "secrets": [
      {
        "name": "RAPIDAPI_KEY",
        "valueFrom": "${rapidapi_ssm_parameter_arn}"
      }
    ]
  }
]
