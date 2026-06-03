data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_vpc" "main" {
  count = var.create_networking ? 1 : 0

  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.tags, {
    Name = "${var.project_name}-vpc"
  })
}

resource "aws_internet_gateway" "main" {
  count = var.create_networking && var.publicly_accessible ? 1 : 0

  vpc_id = aws_vpc.main[0].id

  tags = merge(var.tags, {
    Name = "${var.project_name}-igw"
  })
}

resource "aws_subnet" "private_a" {
  count = var.create_networking ? 1 : 0

  vpc_id                  = aws_vpc.main[0].id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = var.publicly_accessible

  tags = merge(var.tags, {
    Name = "${var.project_name}-db-a"
  })
}

resource "aws_subnet" "private_b" {
  count = var.create_networking ? 1 : 0

  vpc_id                  = aws_vpc.main[0].id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = data.aws_availability_zones.available.names[1]
  map_public_ip_on_launch = var.publicly_accessible

  tags = merge(var.tags, {
    Name = "${var.project_name}-db-b"
  })
}

resource "aws_route_table" "public" {
  count = var.create_networking && var.publicly_accessible ? 1 : 0

  vpc_id = aws_vpc.main[0].id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main[0].id
  }

  tags = merge(var.tags, {
    Name = "${var.project_name}-public"
  })
}

resource "aws_route_table_association" "db_a" {
  count = var.create_networking && var.publicly_accessible ? 1 : 0

  subnet_id      = aws_subnet.private_a[0].id
  route_table_id = aws_route_table.public[0].id
}

resource "aws_route_table_association" "db_b" {
  count = var.create_networking && var.publicly_accessible ? 1 : 0

  subnet_id      = aws_subnet.private_b[0].id
  route_table_id = aws_route_table.public[0].id
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnets"
  subnet_ids = local.subnet_ids

  lifecycle {
    precondition {
      condition = var.create_networking || (
        var.vpc_id != null && length(var.subnet_ids) >= 2
      )
      error_message = "When create_networking is false, set vpc_id and at least two subnet_ids."
    }
  }

  tags = merge(var.tags, {
    Name = "${var.project_name}-db-subnets"
  })
}
