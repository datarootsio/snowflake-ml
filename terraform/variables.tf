variable "snowflake_username" {
  description = "Snowflake user."
  type        = string
}

variable "snowflake_role" {
  description = "Snowflake user role."
  type        = string
}

variable "snowflake_account" {
  description = "Snowflake account name."
  type        = string
}

variable "snowflake_region" {
  description = "Snowflake account region."
  type        = string
  sensitive   = true
}

variable "snowflake_private_key" {
  description = "Snowflake user private key."
  type        = string
  sensitive   = true
}

variable "snowflake_private_key_passphrase" {
  description = "Snowflake user private key passphrase."
  type        = string
  sensitive   = true
}

variable "snowflake_confluent_user_rsa_key_public" {
  description = "RSA public key for Confluent user in Snowflake."
  type        = string
  sensitive   = true
}
