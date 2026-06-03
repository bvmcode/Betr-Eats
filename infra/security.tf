resource "aws_security_group" "rds" {
  name        = "${var.project_name}-rds"
  description = "Allow PostgreSQL access to RDS"
  vpc_id      = local.vpc_id

  ingress {
    description = "PostgreSQL"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.project_name}-rds"
  })
}

resource "aws_security_group" "ecs_streamlit" {
  count = var.enable_streamlit_service ? 1 : 0

  name        = "${var.project_name}-ecs-streamlit"
  description = "Allow public Streamlit access and outbound traffic for ECS tasks"
  vpc_id      = local.vpc_id

  ingress {
    description = "Streamlit"
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = var.streamlit_allowed_cidr_blocks
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.project_name}-ecs-streamlit"
  })
}

resource "aws_security_group_rule" "rds_from_ecs" {
  count = var.enable_streamlit_service ? 1 : 0

  type                     = "ingress"
  description              = "PostgreSQL from Streamlit ECS tasks"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = aws_security_group.rds.id
  source_security_group_id = aws_security_group.ecs_streamlit[0].id
}
