terraform {
  required_version = "~>1.0.0"
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~>0.37.1"
    }
  }
}

provider "snowflake" {
  username               = var.snowflake_username
  role                   = var.snowflake_role
  account                = var.snowflake_account
  region                 = var.snowflake_region
  private_key            = var.snowflake_private_key
  private_key_passphrase = var.snowflake_private_key_passphrase
}


data "snowflake_current_account" "this" {}

output "snowflake_account_url" {
  value = data.snowflake_current_account.this.url
}
