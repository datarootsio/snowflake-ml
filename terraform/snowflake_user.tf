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

resource "snowflake_user" "streamlit" {
  name         = "Streamlit user"
  login_name   = "streamlit"
  comment      = "A user for streamlit app."
  password     = var.streamlit_password
  disabled     = false
  display_name = "Streamlit"

  default_warehouse    = snowflake_warehouse.reddit_xs.name
  default_role         = snowflake_role.streamlit.name
  must_change_password = false
}

resource "snowflake_role" "streamlit" {
  name    = "STREAMLIT_ROLE"
  comment = "Allows users to display data in Streamlit applications."
}

resource "snowflake_role_grants" "streamlit_grants" {
  role_name = snowflake_role.streamlit.name
  users = [
    snowflake_user.streamlit.name
  ]
  depends_on = [snowflake_role.streamlit]
}
