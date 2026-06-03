resource "random_password" "db" {
  count = var.db_password == null ? 1 : 0

  length  = 32
  special = false
}

resource "aws_db_parameter_group" "main" {
  name   = "${var.project_name}-postgres16"
  family = "postgres16"

  tags = var.tags
}

resource "aws_db_instance" "main" {
  identifier = "${var.project_name}-postgres"

  engine         = "postgres"
  engine_version = "16"
  instance_class = var.instance_class

  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = var.db_name
  username = var.db_username
  password = local.db_password

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  parameter_group_name   = aws_db_parameter_group.main.name

  publicly_accessible     = var.publicly_accessible
  skip_final_snapshot     = var.skip_final_snapshot
  deletion_protection     = var.deletion_protection
  backup_retention_period = var.backup_retention_period

  tags = merge(var.tags, {
    Name = "${var.project_name}-postgres"
  })
}
