output "account" {
  value = data.snowflake_current_account.this
}

output "mat_views" {
  value = data.snowflake_materialized_views.reddit
}

output "functions" {
  value = data.snowflake_functions.reddit
}
