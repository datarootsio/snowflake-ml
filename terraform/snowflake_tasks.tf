resource "snowflake_task" "get_new_posts" {
  comment = "Extract, unpack and cast values of new posts from landing tables."

  database  = snowflake_database.snowflake_ml.name
  schema    = snowflake_schema.reddit.name
  warehouse = snowflake_warehouse.reddit_xs.name

  name               = "GET_NEW_POSTS"
  schedule           = "USING CRON */5 * * * 1-5 Europe/Brussels"
  sql_statement      = file("${path.module}/../sql/tasks/get_new_posts.sql")
  session_parameters = {}

  when    = "system$stream_has_data('${snowflake_stream.new_posts.name}')"
  enabled = false
}

resource "snowflake_task" "clean_ml_posts" {
  comment = "Clean post titles - remove non-ASCII characters from post title."

  database  = snowflake_database.snowflake_ml.name
  schema    = snowflake_schema.reddit.name
  warehouse = snowflake_warehouse.reddit_xs.name

  name          = "CLEAN_ML_POSTS"
  sql_statement = file("${path.module}/../sql/tasks/clean_ml_posts.sql")

  after   = "GET_NEW_POSTS"
  when    = "system$stream_has_data('${snowflake_stream.new_ml_posts.name}')"
  enabled = true
}
resource "snowflake_task" "predict_ml_posts" {
  comment = "Run inference to find toxic post titles."

  database  = snowflake_database.snowflake_ml.name
  schema    = snowflake_schema.reddit.name
  warehouse = snowflake_warehouse.reddit_xs.name

  name          = "PREDICT_ML_POSTS"
  sql_statement = file("${path.module}/../sql/tasks/predict_ml_posts.sql")

  after   = "CLEAN_ML_POSTS"
  when    = "system$stream_has_data('${snowflake_stream.new_ml_posts_clean.name}')"
  enabled = true
}

resource "snowflake_stream" "new_posts" {
  comment = "Watch for new posts coming from Confluent tables."

  database = snowflake_database.snowflake_ml.name
  schema   = snowflake_schema.reddit.name
  name     = "NEW_POSTS"

  on_table    = "${snowflake_table.posts.database}.${snowflake_table.posts.schema}.${snowflake_table.posts.name}"
  append_only = true
  insert_only = false
}

resource "snowflake_stream" "new_ml_posts" {
  comment = "Watch for new entries in `ML_POSTS`."

  database = snowflake_database.snowflake_ml.name
  schema   = snowflake_schema.reddit.name
  name     = "NEW_ML_POSTS"

  on_table    = "${snowflake_table.ml_posts.database}.${snowflake_table.ml_posts.schema}.${snowflake_table.ml_posts.name}"
  append_only = true
  insert_only = false
}

resource "snowflake_stream" "new_ml_posts_clean" {
  comment = "Watch for new entries in `ML_POSTS_CLEAN`."

  database = snowflake_database.snowflake_ml.name
  schema   = snowflake_schema.reddit.name
  name     = "NEW_ML_POSTS_CLEAN"

  on_table    = "${snowflake_table.ml_posts_clean.database}.${snowflake_table.ml_posts_clean.schema}.${snowflake_table.ml_posts_clean.name}"
  append_only = true
  insert_only = false
}
