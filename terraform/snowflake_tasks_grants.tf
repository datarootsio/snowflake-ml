resource "snowflake_task_grant" "get_new_posts" {
  database_name = snowflake_task.get_new_posts.database
  schema_name   = snowflake_task.get_new_posts.schema
  task_name     = snowflake_task.get_new_posts.name

  privilege = "OWNERSHIP"
  roles = [
    data.snowflake_role.accountadmin.name
  ]

  on_future         = false
  with_grant_option = true
}

resource "snowflake_task_grant" "clean_ml_posts" {
  database_name = snowflake_task.clean_ml_posts.database
  schema_name   = snowflake_task.clean_ml_posts.schema
  task_name     = snowflake_task.clean_ml_posts.name

  privilege = "OWNERSHIP"
  roles = [
    data.snowflake_role.accountadmin.name
  ]

  on_future         = false
  with_grant_option = true
}

resource "snowflake_task_grant" "predict_ml_posts" {
  database_name = snowflake_task.predict_ml_posts.database
  schema_name   = snowflake_task.predict_ml_posts.schema
  task_name     = snowflake_task.predict_ml_posts.name

  privilege = "OWNERSHIP"
  roles = [
    data.snowflake_role.accountadmin.name
  ]

  on_future         = false
  with_grant_option = true
}

resource "snowflake_stream_grant" "new_posts" {
  database_name = snowflake_stream.new_posts.database
  schema_name   = snowflake_stream.new_posts.schema
  stream_name   = snowflake_stream.new_posts.name

  privilege = "OWNERSHIP"
  roles = [
    data.snowflake_role.accountadmin.name
  ]

  on_future         = false
  with_grant_option = true
}

resource "snowflake_stream_grant" "new_ml_posts" {
  database_name = snowflake_stream.new_ml_posts.database
  schema_name   = snowflake_stream.new_ml_posts.schema
  stream_name   = snowflake_stream.new_ml_posts.name

  privilege = "OWNERSHIP"
  roles = [
    data.snowflake_role.accountadmin.name
  ]

  on_future         = false
  with_grant_option = true
}

resource "snowflake_stream_grant" "new_ml_posts_clean" {
  database_name = snowflake_stream.new_ml_posts_clean.database
  schema_name   = snowflake_stream.new_ml_posts_clean.schema
  stream_name   = snowflake_stream.new_ml_posts_clean.name

  privilege = "OWNERSHIP"
  roles = [
    data.snowflake_role.accountadmin.name
  ]

  on_future         = false
  with_grant_option = true
}
