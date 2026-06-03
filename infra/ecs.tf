

resource "aws_cloudwatch_log_group" "streamlit" {
  count = var.enable_streamlit_service ? 1 : 0

  name              = "/ecs/${var.project_name}-streamlit"
  retention_in_days = var.streamlit_log_retention_days

  tags = var.tags
}

resource "aws_iam_role" "ecs_execution" {
  count = var.enable_streamlit_service ? 1 : 0

  name = "${var.project_name}-ecs-execution"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "ecs_execution" {
  count = var.enable_streamlit_service ? 1 : 0

  role       = aws_iam_role.ecs_execution[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_cluster" "main" {
  count = var.enable_streamlit_service ? 1 : 0

  name = "${var.project_name}-cluster"

  setting {
    name  = "containerInsights"
    value = "disabled"
  }

  tags = merge(var.tags, {
    Name = "${var.project_name}-cluster"
  })
}

resource "aws_ecs_task_definition" "streamlit" {
  count = var.enable_streamlit_service ? 1 : 0

  family                   = "${var.project_name}-streamlit"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.streamlit_cpu
  memory                   = var.streamlit_memory
  execution_role_arn       = aws_iam_role.ecs_execution[0].arn

  container_definitions = jsonencode([{
    name      = "streamlit"
    image     = "${var.aws_account_id}.dkr.ecr.us-east-1.amazonaws.com/betr-eats:latest"
    essential = true

    portMappings = [{
      containerPort = 8501
      hostPort      = 8501
      protocol      = "tcp"
    }]

    environment = concat(
      [
        { name = "POSTGRES_HOST", value = aws_db_instance.main.address },
        { name = "POSTGRES_PORT", value = tostring(aws_db_instance.main.port) },
        { name = "POSTGRES_USER", value = aws_db_instance.main.username },
        { name = "POSTGRES_DB", value = aws_db_instance.main.db_name },
        { name = "POSTGRES_PASSWORD", value = local.db_password },
        { name = "HF_MODEL", value = var.hf_model },
        { name = "STREAMLIT_SERVER_HEADLESS", value = "true" },
        { name = "STREAMLIT_SERVER_ADDRESS", value = "0.0.0.0" },
        { name = "STREAMLIT_SERVER_PORT", value = "8501" },
        { name = "ENV", value = "prod" },
      ],
      var.hf_token == null ? [] : [{ name = "HF_TOKEN", value = var.hf_token }],
    )

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.streamlit[0].name
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "streamlit"
      }
    }
  }])

  tags = var.tags
}

resource "aws_ecs_service" "streamlit" {
  count = var.enable_streamlit_service ? 1 : 0

  name            = "${var.project_name}-streamlit"
  cluster         = aws_ecs_cluster.main[0].id
  task_definition = aws_ecs_task_definition.streamlit[0].arn
  desired_count   = var.streamlit_desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = local.subnet_ids
    security_groups  = [aws_security_group.ecs_streamlit[0].id]
    assign_public_ip = var.streamlit_assign_public_ip
  }

  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 100

  lifecycle {
    precondition {
      condition     = !var.streamlit_assign_public_ip || var.publicly_accessible
      error_message = "streamlit_assign_public_ip requires publicly_accessible = true so the VPC has an internet gateway and public routes."
    }
  }

  depends_on = [
    aws_security_group_rule.rds_from_ecs,
    aws_iam_role_policy_attachment.ecs_execution,
  ]

  tags = merge(var.tags, {
    Name = "${var.project_name}-streamlit"
  })
}
