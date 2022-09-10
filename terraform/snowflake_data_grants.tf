
resource "snowflake_database_grant" "snowflake_ml" {
  database_name = snowflake_database.snowflake_ml.name

  privilege = "USAGE"
  roles     = [snowflake_role.confluent.name]
}

resource "snowflake_schema_grant" "reddit_usage" {
  database_name = snowflake_schema.reddit.database
  schema_name   = snowflake_schema.reddit.name

  privilege = "USAGE"
  roles     = [snowflake_role.confluent.name]
}

resource "snowflake_schema_grant" "reddit_create_materialized_view" {
  database_name = snowflake_schema.reddit.database
  schema_name   = snowflake_schema.reddit.name

  privilege = "CREATE MATERIALIZED VIEW"
  roles     = [snowflake_role.confluent.name]
}

resource "snowflake_schema_grant" "reddit_create_table" {
  database_name = snowflake_schema.reddit.database
  schema_name   = snowflake_schema.reddit.name

  privilege = "CREATE TABLE"
  roles     = [snowflake_role.confluent.name]
}

resource "snowflake_schema_grant" "reddit_create_stage" {
  database_name = snowflake_schema.reddit.database
  schema_name   = snowflake_schema.reddit.name

  privilege = "CREATE STAGE"
  roles     = [snowflake_role.confluent.name]
}

resource "snowflake_schema_grant" "reddit_create_pipe" {
  database_name = snowflake_schema.reddit.database
  schema_name   = snowflake_schema.reddit.name

  privilege = "CREATE PIPE"
  roles     = [snowflake_role.confluent.name]
}

resource "snowflake_table_grant" "comments_ownership" {
  database_name = snowflake_table.comments.database
  schema_name   = snowflake_table.comments.schema
  table_name    = snowflake_table.comments.name

  privilege = "OWNERSHIP"
  roles = [
    snowflake_role.confluent.name,
    # data.snowflake_role.accountadmin.name  # Cannot assign 2 roles
  ]
  shares = []
}

resource "snowflake_table_grant" "posts_ownership" {
  database_name = snowflake_table.posts.database
  schema_name   = snowflake_table.posts.schema
  table_name    = snowflake_table.posts.name

  privilege = "OWNERSHIP"
  roles = [
    snowflake_role.confluent.name,
    # data.snowflake_role.accountadmin.name  # Cannot assign 2 roles
  ]
  shares = []
}

resource "snowflake_table_grant" "comments_select" {
  database_name = snowflake_table.comments.database
  schema_name   = snowflake_table.comments.schema
  table_name    = snowflake_table.comments.name

  privilege = "SELECT"
  roles     = [data.snowflake_role.accountadmin.name]
  shares    = []
}

resource "snowflake_table_grant" "posts_select" {
  database_name = snowflake_table.posts.database
  schema_name   = snowflake_table.posts.schema
  table_name    = snowflake_table.posts.name

  privilege = "SELECT"
  roles     = [data.snowflake_role.accountadmin.name]
  shares    = []
}

resource "snowflake_materialized_view_grant" "flattened_comments" {
  database_name          = snowflake_database.snowflake_ml.name
  schema_name            = snowflake_schema.reddit.name
  materialized_view_name = "FLATTENED_COMMENTS"

  privilege = "OWNERSHIP"
  roles     = [data.snowflake_role.accountadmin.name]
  shares    = []
}

resource "snowflake_view_grant" "posts_typed" {
  database_name = snowflake_view.posts_typed.database
  schema_name   = snowflake_view.posts_typed.schema
  view_name     = snowflake_view.posts_typed.name

  privilege = "OWNERSHIP"
  roles     = [data.snowflake_role.accountadmin.name]
  shares    = []
}

resource "snowflake_view_grant" "comments_typed" {
  database_name = snowflake_view.comments_typed.database
  schema_name   = snowflake_view.comments_typed.schema
  view_name     = snowflake_view.comments_typed.name

  privilege = "OWNERSHIP"
  roles     = [data.snowflake_role.accountadmin.name]
  shares    = []
}

resource "snowflake_view_grant" "posts_aggregated" {
  database_name = snowflake_view.posts_aggregated.database
  schema_name   = snowflake_view.posts_aggregated.schema
  view_name     = snowflake_view.posts_aggregated.name

  privilege = "OWNERSHIP"
  roles     = [data.snowflake_role.accountadmin.name]
  shares    = []
}

resource "snowflake_view_grant" "comments_aggregated" {
  database_name = snowflake_view.comments_typed.database
  schema_name   = snowflake_view.comments_typed.schema
  view_name     = snowflake_view.comments_typed.name

  privilege = "OWNERSHIP"
  roles     = [data.snowflake_role.accountadmin.name]
  shares    = []
}

resource "snowflake_table_grant" "ml_posts" {
  database_name = snowflake_table.ml_posts.database
  schema_name   = snowflake_table.ml_posts.schema
  table_name    = snowflake_table.ml_posts.name

  with_grant_option = true
  privilege         = "OWNERSHIP"
  roles             = [data.snowflake_role.accountadmin.name]
  shares            = []
}

resource "snowflake_table_grant" "ml_posts_clean" {
  database_name = snowflake_table.ml_posts_clean.database
  schema_name   = snowflake_table.ml_posts_clean.schema
  table_name    = snowflake_table.ml_posts_clean.name

  with_grant_option = true
  privilege         = "OWNERSHIP"
  roles             = [data.snowflake_role.accountadmin.name]
  shares            = []
}

resource "snowflake_table_grant" "ml_posts_toxic" {
  database_name = snowflake_table.ml_posts_toxic.database
  schema_name   = snowflake_table.ml_posts_toxic.schema
  table_name    = snowflake_table.ml_posts_toxic.name

  with_grant_option = true
  privilege         = "OWNERSHIP"
  roles             = [data.snowflake_role.accountadmin.name]
  shares            = []
}
