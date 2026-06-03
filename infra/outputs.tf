output "db_endpoint" {
  description = "RDS instance hostname."
  value       = aws_db_instance.main.address
}

output "db_port" {
  description = "RDS instance port."
  value       = aws_db_instance.main.port
}

output "db_name" {
  description = "Database name."
  value       = aws_db_instance.main.db_name
}

output "db_username" {
  description = "Master database username."
  value       = aws_db_instance.main.username
}

output "db_password" {
  description = "Master database password."
  value       = local.db_password
  sensitive   = true
}

output "connection_string" {
  description = "PostgreSQL connection URI for application use."
  value       = "postgresql://${aws_db_instance.main.username}:${local.db_password}@${aws_db_instance.main.address}:${aws_db_instance.main.port}/${aws_db_instance.main.db_name}?sslmode=require"
  sensitive   = true
}

output "vpc_id" {
  description = "VPC ID used by RDS."
  value       = local.vpc_id
}

output "ecs_cluster_name" {
  description = "ECS cluster running the Streamlit service."
  value       = var.enable_streamlit_service ? aws_ecs_cluster.main[0].name : null
}

output "ecs_service_name" {
  description = "ECS service name for the Streamlit app."
  value       = var.enable_streamlit_service ? aws_ecs_service.streamlit[0].name : null
}

output "streamlit_public_ip_command" {
  description = "Shell command to print the public IP of a running Streamlit task."
  value = var.enable_streamlit_service ? join(" ", [
    "${path.module}/scripts/streamlit_public_ip.sh",
    aws_ecs_cluster.main[0].name,
    aws_ecs_service.streamlit[0].name,
  ]) : null
}
