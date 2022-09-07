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
  change_tracking     = true
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
  change_tracking     = true

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

  statement  = file("${path.module}/../sql/flattened_comments_typed.sql")
  or_replace = true
  is_secure  = false
}

resource "snowflake_view" "posts_aggregated" {
  database = snowflake_schema.reddit.database
  schema   = snowflake_schema.reddit.name
  name     = "AGGREGATED_POSTS"
  comment  = "Aggregate posts to number of records, average length of title and body."

  statement  = file("${path.module}/../sql/aggregated_posts.sql")
  or_replace = true
  is_secure  = false
}

resource "snowflake_view" "comments_aggregated" {
  database = snowflake_schema.reddit.database
  schema   = snowflake_schema.reddit.name
  name     = "AGGREGATED_COMMENTS"
  comment  = "Aggregate comments to number of records, average length of title and body."

  statement  = file("${path.module}/../sql/aggregated_comments.sql")
  or_replace = true
  is_secure  = false
}


#TODO
resource "snowflake_table" "ml_posts" {
  database = snowflake_schema.reddit.database
  schema   = snowflake_schema.reddit.name
  name     = "ML_POSTS"
  #  comment             = "Reddit posts data."
  data_retention_days = snowflake_schema.reddit.data_retention_days
  change_tracking     = true

  column {
    name     = "RECORD_ID"
    nullable = true
    type     = "VARCHAR(16777216)"
  }
  column {
    name     = "CREATED_TIMESTAMP"
    nullable = true
    type     = "TIMESTAMP_NTZ(9)"
  }
  column {
    name     = "SUBREDDIT"
    nullable = true
    type     = "VARCHAR(16777216)"
  }
  column {
    name     = "AUTHOR"
    nullable = true
    type     = "VARCHAR(16777216)"
  }
  column {
    name     = "TITLE"
    nullable = true
    type     = "VARCHAR(16777216)"
  }
}
resource "snowflake_table" "ml_posts_clean" {
  database = snowflake_schema.reddit.database
  schema   = snowflake_schema.reddit.name
  name     = "ML_POSTS_CLEAN"
  #  comment             = "Reddit posts data."
  data_retention_days = snowflake_schema.reddit.data_retention_days
  change_tracking     = true

  column {
    name     = "RECORD_ID"
    nullable = true
    type     = "VARCHAR(16777216)"
  }
  column {
    name     = "CREATED_TIMESTAMP"
    nullable = true
    type     = "TIMESTAMP_NTZ(9)"
  }
  column {
    name     = "SUBREDDIT"
    nullable = true
    type     = "VARCHAR(16777216)"
  }
  column {
    name     = "AUTHOR"
    nullable = true
    type     = "VARCHAR(16777216)"
  }
  column {
    name     = "TITLE"
    nullable = true
    type     = "VARCHAR(16777216)"
  }
}
resource "snowflake_table" "ml_posts_predictions" {
  database = snowflake_schema.reddit.database
  schema   = snowflake_schema.reddit.name
  name     = "ML_POSTS_PREDICTIONS"
  #  comment             = "Reddit posts data."
  data_retention_days = snowflake_schema.reddit.data_retention_days
  change_tracking     = false

  column {
    name     = "RECORD_ID"
    nullable = true
    type     = "VARCHAR(16777216)"
  }
  column {
    name     = "CREATED_TIMESTAMP"
    nullable = true
    type     = "TIMESTAMP_NTZ(9)"
  }
  column {
    name     = "SUBREDDIT"
    nullable = true
    type     = "VARCHAR(16777216)"
  }
  column {
    name     = "AUTHOR"
    nullable = true
    type     = "VARCHAR(16777216)"
  }
  column {
    name     = "TITLE"
    nullable = true
    type     = "VARCHAR(16777216)"
  }
  column {
    name     = "IS_TOXIC"
    nullable = true
    type     = "NUMBER(38,0)"
  }
  column {
    name     = "MODEL_VERSION"
    nullable = true
    type     = "VARCHAR(16777216)"
  }
}
