data "snowflake_role" "accountadmin" {
  name = "accountadmin"
}

resource "snowflake_user" "confluent" {
  name                 = "CONFLUENT_USER"
  comment              = "Confluent user for streaming data."
  default_role         = snowflake_role.confluent.name
  must_change_password = false
  rsa_public_key       = var.snowflake_confluent_user_rsa_key_public
}

resource "snowflake_role" "confluent" {
  name    = "CONFLUENT_ROLE"
  comment = "Confluent user role for streaming data."
}

resource "snowflake_role_grants" "confluent_grants" {
  role_name = snowflake_role.confluent.name
  users = [
    snowflake_user.confluent.name
  ]
}
