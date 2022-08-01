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

# Could not create in terraform, nor create manually and import
# https://github.com/Snowflake-Labs/terraform-provider-snowflake/issues/818
#resource "snowflake_materialized_view" "flattened_comments" {
#    database = snowflake_schema.reddit.database
#  schema   = snowflake_schema.reddit.name
#  warehouse = snowflake_warehouse.reddit_xs.name
#  name      = "FLATTENED_COMMENTS"
#
#  statement  = file("${path.module}/../sql/flattened_comments.sql")
#  or_replace = true
#}

data "snowflake_materialized_views" "reddit" {
  database = snowflake_schema.reddit.database
  schema   = snowflake_schema.reddit.name
}

resource "snowflake_view" "posts_typed" {
  database = snowflake_schema.reddit.database
  schema   = snowflake_schema.reddit.name
  name     = "POSTS_TYPED"
  comment  = "Add the correct types to the flattened JSON from Reddit's posts data."

  statement  = file("${path.module}/../sql/flattened_posts_typed.sql")
  or_replace = true
  is_secure  = false
}

resource "snowflake_view" "comments_typed" {
  database = snowflake_schema.reddit.database
  schema   = snowflake_schema.reddit.name
  name     = "COMMENTS_TYPED"
  comment  = "Add the correct types to the flattened JSON from Reddit's comment data."

  statement = file("${path.module}/../sql/flattened_comments_typed.sql")

  or_replace = true
  is_secure  = false
}
