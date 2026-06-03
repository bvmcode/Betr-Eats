resource "terraform_data" "schema" {
  depends_on = [aws_db_instance.main]

  input = filemd5("${path.module}/init.sql")

  provisioner "local-exec" {
    when = create
    environment = {
      PGPASSWORD = local.db_password
    }
    command = join(" ", [
      "${path.module}/scripts/apply_schema.sh",
      aws_db_instance.main.address,
      tostring(aws_db_instance.main.port),
      aws_db_instance.main.db_name,
      aws_db_instance.main.username,
      "${path.module}/init.sql",
    ])
  }
}
