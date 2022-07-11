FROM confluentinc/cp-kafka-connect-base:7.1.2

COPY docker/C0urante-kafka-connect-reddit-0.1.3.zip /tmp/C0urante-kafka-connect-reddit-0.1.3.zip
COPY docker/kafka-connect-reddit-source.properties  /etc/kafka/kafka-connect-reddit-source.properties
COPY docker/connect-to-confluent-standalone.properties  /etc/kafka/connect-to-confluent-standalone.properties

RUN confluent-hub install --no-prompt /tmp/C0urante-kafka-connect-reddit-0.1.3.zip

CMD ["connect-standalone", "/etc/kafka/connect-to-confluent-standalone.properties", "/etc/kafka/kafka-connect-reddit-source.properties"]
