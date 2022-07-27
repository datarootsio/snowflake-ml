resource "snowflake_database" "snowflake_ml" {
  name                        = "SNOWFLAKE_ML"
  comment                     = "Sample database for Snowflake ML use-case."
  data_retention_time_in_days = 1
}

resource "snowflake_schema" "reddit" {
  database            = snowflake_database.snowflake_ml.name
  name                = "REDDIT"
  data_retention_days = snowflake_database.snowflake_ml.data_retention_time_in_days
}

resource "snowflake_table" "comments" {
  database            = snowflake_schema.reddit.database
  schema              = snowflake_schema.reddit.name
  name                = "SNOWFLAKE_ML_REDDIT_COMMENTS_423303504"
  comment             = "Reddit comments data."
  data_retention_days = snowflake_schema.reddit.data_retention_days
  change_tracking     = false
  column {
    name = "RECORD_METADATA"
    type = "VARIANT"
  }
  column {
    name     = "RECORD_CONTENT"
    nullable = true
    type     = "VARIANT"
  }

}

resource "snowflake_table" "posts" {
  database            = snowflake_schema.reddit.database
  schema              = snowflake_schema.reddit.name
  name                = "SNOWFLAKE_ML_REDDIT_POSTS_1911518057"
  comment             = "Reddit posts data."
  data_retention_days = snowflake_schema.reddit.data_retention_days
  change_tracking     = false

  column {
    name     = "RECORD_METADATA"
    nullable = true
    type     = "VARIANT"
  }
  column {
    name     = "RECORD_CONTENT"
    nullable = true
    type     = "VARIANT"
  }
}


resource "snowflake_database_grant" "snowflake_ml" {
  database_name = snowflake_database.snowflake_ml.name

  privilege = "USAGE"
  roles     = [snowflake_role.confluent.name]
}

resource "snowflake_schema_grant" "reddit_usage" {
  database_name = snowflake_database.snowflake_ml.name
  schema_name   = snowflake_schema.reddit.name

  privilege = "USAGE"
  roles     = [snowflake_role.confluent.name]
}

resource "snowflake_schema_grant" "reddit_create_table" {
  database_name = snowflake_database.snowflake_ml.name
  schema_name   = snowflake_schema.reddit.name

  privilege = "CREATE TABLE"
  roles     = [snowflake_role.confluent.name]
}

resource "snowflake_schema_grant" "reddit_create_stage" {
  database_name = snowflake_database.snowflake_ml.name
  schema_name   = snowflake_schema.reddit.name

  privilege = "CREATE STAGE"
  roles     = [snowflake_role.confluent.name]
}

resource "snowflake_schema_grant" "reddit_create_pipe" {
  database_name = snowflake_database.snowflake_ml.name
  schema_name   = snowflake_schema.reddit.name

  privilege = "CREATE PIPE"
  roles     = [snowflake_role.confluent.name]
}

resource "snowflake_table_grant" "comments" {
  database_name = snowflake_database.snowflake_ml.name
  schema_name   = snowflake_schema.reddit.name
  table_name    = snowflake_table.comments.name

  privilege = "OWNERSHIP"
  roles     = [snowflake_role.confluent.name]
  shares    = []
}

resource "snowflake_table_grant" "posts" {
  database_name = snowflake_database.snowflake_ml.name
  schema_name   = snowflake_schema.reddit.name
  table_name    = snowflake_table.posts.name

  privilege = "OWNERSHIP"
  roles     = [snowflake_role.confluent.name]
  shares    = []
}
