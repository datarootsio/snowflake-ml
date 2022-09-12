resource "confluent_environment" "default" {
  display_name = "default"
}

resource "confluent_kafka_cluster" "cluster_snowflake_ml" {
  display_name = "cluster_snowflake_ml"
  availability = "SINGLE_ZONE"
  cloud        = "AWS"
  region       = "eu-central-1"
  basic {}

  environment {
    id = confluent_environment.default.id
  }
}

resource "confluent_kafka_topic" "reddit_comments" {
  kafka_cluster {
    id = confluent_kafka_cluster.cluster_snowflake_ml.id
  }
  topic_name       = "snowflake-ml-reddit-comments"
  partitions_count = 6
  config = {
    "cleanup.policy"                      = "delete"
    "max.message.bytes"                   = "2097164"
    "retention.ms"                        = "604800000"
    "delete.retention.ms"                 = "86400000"
    "max.compaction.lag.ms"               = "9223372036854775807"
    "message.timestamp.difference.max.ms" = "9223372036854775807"
    "message.timestamp.type"              = "CreateTime"
    "min.compaction.lag.ms"               = "0"
    "min.insync.replicas"                 = "2"
    "retention.bytes"                     = "-1"
    "segment.bytes"                       = "104857600"
    "segment.ms"                          = "604800000"
  }
}

resource "confluent_kafka_topic" "reddit_posts" {
  kafka_cluster {
    id = confluent_kafka_cluster.cluster_snowflake_ml.id
  }
  topic_name       = "snowflake-ml-reddit-posts"
  partitions_count = 6
  config = {
    "cleanup.policy"                      = "delete"
    "max.message.bytes"                   = "2097164"
    "retention.ms"                        = "604800000"
    "delete.retention.ms"                 = "86400000"
    "max.compaction.lag.ms"               = "9223372036854775807"
    "message.timestamp.difference.max.ms" = "9223372036854775807"
    "message.timestamp.type"              = "CreateTime"
    "min.compaction.lag.ms"               = "0"
    "min.insync.replicas"                 = "2"
    "retention.bytes"                     = "-1"
    "segment.bytes"                       = "104857600"
    "segment.ms"                          = "604800000"
  }
}

resource "confluent_connector" "snowflake" {
  status = "PAUSED" # Change to "RUNNING"

  environment {
    id = confluent_environment.default.id
  }
  kafka_cluster {
    id = confluent_kafka_cluster.cluster_snowflake_ml.id
  }

  config_sensitive = {}

  config_nonsensitive = {
    "connector.class"         = "SnowflakeSink"
    "input.data.format"       = "JSON"
    "name"                    = "SnowflakeSinkConnector_0"
    "kafka.auth.mode"         = "KAFKA_API_KEY"
    "tasks.max"               = "1"
    "snowflake.database.name" = snowflake_database.snowflake_ml.name
    "snowflake.schema.name"   = snowflake_schema.reddit.name
    "snowflake.url.name"      = data.snowflake_current_account.this.url
    "snowflake.user.name"     = snowflake_user.confluent.name
    "topics"                  = "snowflake-ml-reddit-comments,snowflake-ml-reddit-posts"

  }
}
