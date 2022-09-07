resource "snowflake_task" "get_new_posts" {
  comment = "Extract, unpack and cast values of new posts from landing tables."

  database  = snowflake_database.snowflake_ml.name
  schema    = snowflake_schema.reddit.name
  warehouse = snowflake_warehouse.reddit_xs.name

  name               = "GET_NEW_POSTS"
  schedule           = "USING CRON */5 * * * 1-5 Europe/Brussels"
  sql_statement      = file("${path.module}/../sql/tasks/get_new_posts.sql")
  session_parameters = {}

  when    = "system$stream_has_data('new_posts')"
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
  when    = "system$stream_has_data('new_ml_posts')"
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
  when    = "system$stream_has_data('new_ml_posts_clean')"
  enabled = true
}
