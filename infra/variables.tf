variable "aws_region" {
  description = "AWS region for RDS and networking."
  type        = string
  default     = "us-east-1"
}

variable "aws_account_id" {
  description = "AWS account ID."
  type        = string
  default     = ""
}

variable "project_name" {
  description = "Prefix used for resource names."
  type        = string
  default     = "betr-eats"
}

variable "db_name" {
  description = "PostgreSQL database name."
  type        = string
  default     = "postgres"
}

variable "db_username" {
  description = "Master username for the RDS instance."
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Master password. Leave null to generate a random password."
  type        = string
  sensitive   = true
  default     = "postgres"
}

variable "instance_class" {
  description = "RDS instance class."
  type        = string
  default     = "db.t4g.micro"
}

variable "allocated_storage" {
  description = "Initial allocated storage in GiB."
  type        = number
  default     = 20
}

variable "max_allocated_storage" {
  description = "Maximum storage for autoscaling in GiB."
  type        = number
  default     = 100
}

variable "backup_retention_period" {
  description = "Number of days to retain automated backups."
  type        = number
  default     = 7
}

variable "publicly_accessible" {
  description = "Whether the RDS instance has a public IP. Set false in production."
  type        = bool
  default     = true
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to connect to PostgreSQL."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "skip_final_snapshot" {
  description = "Skip a final snapshot when destroying the instance."
  type        = bool
  default     = true
}

variable "deletion_protection" {
  description = "Prevent accidental deletion of the RDS instance."
  type        = bool
  default     = false
}

variable "create_networking" {
  description = "Create a dedicated VPC and subnets for RDS."
  type        = bool
  default     = true
}

variable "vpc_id" {
  description = "Existing VPC ID when create_networking is false."
  type        = string
  default     = null
}

variable "subnet_ids" {
  description = "Existing private subnet IDs when create_networking is false."
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "Tags applied to created resources."
  type        = map(string)
  default = {
    Project = "betr-eats"
  }
}

variable "enable_streamlit_service" {
  description = "Create an ECS Fargate service for the Streamlit frontend."
  type        = bool
  default     = true
}

variable "streamlit_image_tag" {
  description = "Docker image tag deployed to the Streamlit ECS service."
  type        = string
  default     = "latest"
}

variable "streamlit_cpu" {
  description = "Fargate CPU units for the Streamlit task (256, 512, 1024, etc.)."
  type        = number
  default     = 512
}

variable "streamlit_memory" {
  description = "Fargate memory in MiB for the Streamlit task."
  type        = number
  default     = 1024
}

variable "streamlit_desired_count" {
  description = "Number of Streamlit tasks to run."
  type        = number
  default     = 1
}

variable "streamlit_assign_public_ip" {
  description = "Assign a public IP to Streamlit tasks for direct internet access."
  type        = bool
  default     = true
}

variable "streamlit_allowed_cidr_blocks" {
  description = "CIDR blocks allowed to reach Streamlit on port 8501."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "streamlit_log_retention_days" {
  description = "CloudWatch log retention for Streamlit ECS tasks."
  type        = number
  default     = 7
}

variable "hf_model" {
  description = "Hugging Face model ID passed to the Streamlit app."
  type        = string
  default     = "deepseek-ai/DeepSeek-V4-Pro:novita"
}

variable "hf_token" {
  description = "Hugging Face API token for the Streamlit app. Leave null to set manually in the task definition later."
  type        = string
  sensitive   = true
  default     = null
}
