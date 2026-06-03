locals {
  #db_password = coalesce(var.db_password, random_password.db[0].result)
  db_password = var.db_password
  vpc_id = var.create_networking ? aws_vpc.main[0].id : var.vpc_id

  subnet_ids = var.create_networking ? [
    aws_subnet.private_a[0].id,
    aws_subnet.private_b[0].id,
  ] : var.subnet_ids
}
