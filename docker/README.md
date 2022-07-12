# Kafka Connect - Reddit

Plugin:
- [Github](https://github.com/C0urante/kafka-connect-reddit)
- [Confluent Hub](https://www.confluent.io/hub/C0urante/kafka-connect-reddit/)

## Standalone mode with docker

We run the Kafka Connect locally, on standalone mode. We install the plugin from the
Confluent Hub as a `zip` and installed them.

> We recommend a distributed approach for production purposes.

The `kafka-connect-reddit.Dockerfile` contains the information necessary for the setup.
Additionally, it is required to add the configuration files.

### `connect-to-confluent-standalone.properties`

Replace the `<kafka-api-key>`, `<kafka-api-secret>`, `<kafka-bootstrap-server>` values
with the ones retrieved from your Confluent Cloud configuration:

```txt
bootstrap.servers=<kafka-bootstrap-server>

# The converters specify the format of data in Kafka and how to translate it into Connect data. Every Connect user will
# need to configure these based on the format they want their data in when loaded from or stored into Kafka
key.converter=org.apache.kafka.connect.json.JsonConverter
value.converter=org.apache.kafka.connect.json.JsonConverter
# Converter-specific settings can be passed in by prefixing the Converter's setting with the converter you want to apply
# it to
key.converter.schemas.enable=false
value.converter.schemas.enable=false

# The internal converter used for offsets and config data is configurable and must be specified, but most users will
# always want to use the built-in default. Offset and config data is never visible outside of Kafka Connect in this format.
internal.key.converter=org.apache.kafka.connect.json.JsonConverter
internal.value.converter=org.apache.kafka.connect.json.JsonConverter
internal.key.converter.schemas.enable=false
internal.value.converter.schemas.enable=false

# Store offsets on local filesystem
offset.storage.file.filename=/tmp/connect.offsets
# Flush much faster than normal, which is useful for testing/debugging
offset.flush.interval.ms=10000

ssl.endpoint.identification.algorithm=https
sasl.mechanism=PLAIN
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required \
username="<kafka-api-key>" password="<kafka-api-secret>";
security.protocol=SASL_SSL

consumer.ssl.endpoint.identification.algorithm=https
consumer.sasl.mechanism=PLAIN
consumer.sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required \
username="<kafka-api-key>" password="<kafka-api-secret>";
consumer.security.protocol=SASL_SSL

producer.ssl.endpoint.identification.algorithm=https
producer.sasl.mechanism=PLAIN
producer.sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required \
username="<kafka-api-key>" password="<kafka-api-secret>";
producer.security.protocol=SASL_SSL

# Set to a list of filesystem paths separated by commas (,) to enable class loading isolation for plugins
# (connectors, converters, transformations).
plugin.path=/usr/share/java,/usr/share/confluent-hub-components

```

### `kafka-connect-reddit-source.properties`

Replace the `<kafka-topic-comments>`, `<kafka-topic-posts>` values with the topic names
defined in Confluent Cloud (in our case, `snowflake-ml-reddit-comments` and
`snowflake-ml-reddit-posts`. respectively). Additionally, we can configure the connector
to source posts and comments for a specific subreddit (currently set to `r/all`):

```txt
# General properties for any connector

connector.class=com.github.c0urante.kafka.connect.reddit.RedditSourceConnector
name=reddit-source
tasks.max=2


# Properties specifically for Reddit source connector
# Posts and comments can be read from r/all
posts.subreddits=all
# They can also be read from a specific subreddit or list of subreddits
comments.subreddits=all

comments.topic=snowflake-ml-reddit-comments
posts.topic=snowflake-ml-reddit-posts
# Enable this for debugging
reddit.log.http.requests=false
```
