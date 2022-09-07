resource "snowflake_task_grant" "get_new_posts" {
  database_name = snowflake_database.snowflake_ml.name
  schema_name   = snowflake_schema.reddit.name
  task_name     = snowflake_task.get_new_posts.name

  privilege = "OWNERSHIP"
  roles = [
    data.snowflake_role.accountadmin.name
  ]

  on_future         = false
  with_grant_option = true
}

resource "snowflake_task_grant" "clean_ml_posts" {
  database_name = snowflake_database.snowflake_ml.name
  schema_name   = snowflake_schema.reddit.name
  task_name     = snowflake_task.clean_ml_posts.name

  privilege = "OWNERSHIP"
  roles = [
    data.snowflake_role.accountadmin.name
  ]

  on_future         = false
  with_grant_option = true
}

resource "snowflake_task_grant" "predict_ml_posts" {
  database_name = snowflake_database.snowflake_ml.name
  schema_name   = snowflake_schema.reddit.name
  task_name     = snowflake_task.predict_ml_posts.name

  privilege = "OWNERSHIP"
  roles = [
    data.snowflake_role.accountadmin.name
  ]

  on_future         = false
  with_grant_option = true
}
