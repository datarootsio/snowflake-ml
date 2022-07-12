terraform {
  required_version = "~>1.0.0"
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~>0.37.1"
    }
    confluent = {
      source  = "confluentinc/confluent"
      version = "1.0.0"
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

provider "confluent" {
  cloud_api_key       = var.confluent_cloud_api_key
  cloud_api_secret    = var.confluent_cloud_api_secret
  kafka_rest_endpoint = var.kafka_rest_endpoint
  kafka_api_key       = var.kafka_api_key
  kafka_api_secret    = var.kafka_api_secret
}

data "snowflake_current_account" "this" {}
