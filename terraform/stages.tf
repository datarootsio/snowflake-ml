data "snowflake_functions" "reddit" {
  database = snowflake_database.snowflake_ml.name
  schema   = snowflake_schema.reddit.name
}
